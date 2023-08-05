import shutil
import queue
import sqlite3
import datetime
from threadwrapper import *
from filehandling import join_path, abs_main_dir
from encryptedsocket import SC as ESC, SS as ESS
from unencryptedsocket import SC as USC, SS as USS
from easyrsa import *
from omnitools import def_template, args, key_pair_format


__ALL__ = ["SqlQueue"]


class SqlQueue(object):
    def worker(self, _db) -> None:
        def connect_db(db):
            conn = sqlite3.connect(db)
            self.__exc(conn, "PRAGMA locking_mode=EXCLUSIVE;")
            return conn
        def disconnect_db(conn):
            self.__exc(conn, "PRAGMA locking_mode=NORMAL;")
            commit_db(conn)
            conn.close()
        def commit_db(conn):
            conn.commit()
            result = self.__exc(conn, "PRAGMA journal_mode;")
            journal_mode = result[0]["journal_mode"]
            if journal_mode == "wal":
                self.__exc(conn, "PRAGMA wal_checkpoint(PASSIVE);")
        def backup(db):
            now = datetime.datetime.now()
            new_db = os.path.join(
                os.path.dirname(db),
                "bak",
                str(now.year),
                str(now.month).zfill(2),
                str(now.day).zfill(2),
                str(now.hour).zfill(2),
                str(now.minute).zfill(2),
                os.path.splitext(os.path.basename(db))[0]+".{}.db".format(int(time.time()*1000))
            )
            os.makedirs(os.path.dirname(new_db), exist_ok=True)
            shutil.copy(db, new_db)
        def do_backup(conn):
            disconnect_db(conn)
            backup(_db)
            self.do_backup = False
            return connect_db(_db)
        timeout_commit = 0
        timeout_backup = 0
        if self.auto_backup:
            backup()
        conn = connect_db(_db)
        while not self.terminate:
            if self.do_commit:
                commit_db(conn)
                self.do_commit = False
            elif self.do_backup:
                conn = do_backup(conn)
            elif self.sqlq.qsize() > 0:
                tid, sql, data, row_factory = self.sqlq.get()
                self.exc_result[tid] = self.__exc(conn, sql, data, row_factory)
                self.sqlq.task_done()
            else:
                if (timeout_commit > self.timeout_commit) and len(self.exc_result) == 0:
                    commit_db(conn)
                    timeout_commit = 0
                else:
                    timeout_commit += 1
                if self.auto_backup and (timeout_backup > self.timeout_backup) and len(self.exc_result) == 0:
                    conn = do_backup(conn)
                    timeout_backup = 0
                else:
                    timeout_backup += 1
            time.sleep(1/1000)
        disconnect_db(conn)
        if self.auto_backup:
            backup(_db)
        self.worker_dead = True

    def __exc(self, conn: sqlite3.Connection, sql: str, data: tuple = (), row_factory: str = "row") -> Any:
        mode = ""
        try:
            if row_factory == "list":
                conn.row_factory = None
            else:
                conn.row_factory = sqlite3.Row
            db = conn.cursor()
            if sql.endswith(";"):
                sql = sql[:-1]
            mode = ""
            if len(data) != 0:
                if isinstance(data[0], list):
                    data = tuple([tuple(_) for _ in data])
                if isinstance(data[0], tuple):
                    mode = "many"
                else:
                    mode = "data"
            elif len(sql.split(";")) > 1:
                mode = "script"
            else:
                mode = "sql"
            if mode == "many":
                db.executemany(sql, data)
            elif mode == "data":
                db.execute(sql, data)
            elif mode == "sql":
                db.execute(sql)
            elif mode == "script":
                db.executescript(sql)
            result = db.fetchall()
            if row_factory == "list":
                result = [list(row) for row in result]
            else:
                result = [dict(row) for row in result]
            return result
        except Exception as e:
            p(f"error: [{mode}] {sql}(", data, f") due to {e}")
            p(debug_info()[0])
            return e

    def backup(self):
        # To-do: client not working
        self.do_backup = True
        while self.do_backup:
            time.sleep(1/1000)

    def commit(self):
        # To-do: client not working
        self.do_commit = True
        while self.do_commit:
            time.sleep(1/1000)

    def stop(self):
        self.terminate = True
        while not self.worker_dead:
            time.sleep(1/1000)

    def __init__(self, server: bool = False, db: str = "", timeout_commit: int = 60*1000, auto_backup: bool = False, timeout_backup: int = 60*1000, depth: int = 2, export_functions = None) -> None:
        self.is_server = server
        self.do_commit = False
        self.do_backup = False
        self.terminate = False
        self.exc_result = {}
        self.timeout_commit = None
        self.auto_backup = None
        self.timeout_backup = None
        self.sqlq = None
        self.sqlq_worker = None
        self.worker_dead = None
        self.functions = None
        self.ioerror = False
        self.exploded_reason = None
        self.sc = None
        if self.is_server:
            if not os.path.isabs(db):
                db = join_path(abs_main_dir(depth=int(depth)), db)
            self.timeout_commit = timeout_commit/20
            self.auto_backup = auto_backup
            self.timeout_backup = timeout_backup/20
            self.sqlq = queue.Queue()
            self.sqlq_worker = threading.Thread(target=self.worker, args=(db,))
            self.sqlq_worker.daemon = True
            self.sqlq_worker.start()
            self.worker_dead = False
            self.functions = dict(sql=self.sql)
            if export_functions:
                self.functions.update(export_functions=export_functions)

    def _sql(self, tid: int, sql: str, data: tuple = (), row_factory: str = "row", _cmd: str = "sql") -> list:
        if self.is_server:
            if _cmd == "sql":
                self.sqlq.put([tid, sql, data, row_factory])
                while tid not in self.exc_result:
                    time.sleep(1/1000)
                    continue
                try:
                    return self.exc_result[tid]
                finally:
                    self.exc_result.pop(tid)
            else:
                try:
                    return self.functions[_cmd](*[sql, data, row_factory])
                except Exception as e:
                    return e
        else:
            return self.sc.request(command=_cmd, data=args(sql, data, row_factory))

    def sql(self, sql: str, data: tuple = (), row_factory: str = "row",
            result: Any = None, key: Any = None, _cmd: str = "sql") -> list:
        if result is None:
            result = {}
        key = key or 0
        try:
            sql = " ".join([line.strip() for line in sql.splitlines() if not line.strip().startswith("--")]).strip()
        except:
            pass

        def job(sql: str, data: tuple, row_factory: str, _cmd: str) -> list:
            return self._sql(threading.get_ident(), sql, data, row_factory, _cmd)

        threadwrapper = ThreadWrapper(threading.Semaphore(1))
        threadwrapper.add(job=def_template(job, sql, data, row_factory, _cmd), result=result, key=key)
        threadwrapper.wait()
        if isinstance(result[key], Exception):
            if isinstance(result[key], sqlite3.OperationalError):
                if "i/o" in str(result[key]).lower():
                    self.ioerror = True
                    try:
                        raise result[key]
                    except:
                        self.exploded_reason = traceback.format_exc()
            raise result[key]
        return result[key]


class SqlQueueE(SqlQueue):
    def __init__(self, db_port: int = None, key_pair: key_pair_format = None, **kwargs) -> None:
        if "db" in kwargs:
            if not os.path.isabs(kwargs["db"]):
                kwargs["db"] = join_path(abs_main_dir(depth=int(kwargs["depth"])), kwargs["db"])
        super().__init__(**kwargs)
        host = "127.199.71.10"
        port = db_port if db_port else 39292
        if self.is_server:
            if key_pair is None:
                key_pair = EasyRSA(bits=1024).gen_key_pair()
            self.ess = ESS(key_pair, self.functions, host, port, True)
            thread = threading.Thread(target=self.ess.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = ESC(host, port)

    def stop(self):
        super().stop()
        self.ess.stop()


class SqlQueueU(SqlQueue):
    def __init__(self, db_port: int = None, **kwargs) -> None:
        if "db" in kwargs:
            if not os.path.isabs(kwargs["db"]):
                kwargs["db"] = join_path(abs_main_dir(depth=int(kwargs["depth"])), kwargs["db"])
        super().__init__(**kwargs)
        host = "127.199.71.10"
        port = db_port if db_port else 39292
        if self.is_server:
            self.uss = USS(self.functions, host, port, True)
            thread = threading.Thread(target=self.uss.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = USC(host, port)

    def stop(self):
        super().stop()
        self.uss.stop()


