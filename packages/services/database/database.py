from .. import ServiceBase
from praqta.interface import ApplicationContext, objdict, Row

# SQLite3用パッケージ
import sqlite3

# PostgreSQL用パッケージ
import psycopg2
from psycopg2.extras import DictCursor

# MySQL用パッケージ
import MySQLdb

import re

from typing import Iterable, cast
from logging import Logger
logger = cast(Logger, {})


class Closer(object):
    def __init__(self, db):
        self.__db = db

    def __enter__(self):
        return self.__db

    def __exit__(self, exception_type, exception_value, traceback):
        self.__db.close()


class CursorIterator(object):
    def __init__(self, cursor):
        self._cursor = cursor
        self._i = 0

    def __iter__(self):
        # __next__()はselfが実装してるのでそのままselfを返す
        return self

    def __next__(self):  # Python2だと next(self) で定義
        row = self._cursor.fetchone()
        if row == None:
            raise StopIteration()
        self._i += 1
        return dict(row)


def open_sqlite(config: dict) -> sqlite3.Connection:
    conf = objdict(config)
    try:
        conn = sqlite3.connect(conf.connect)
        conn.row_factory = sqlite3.Row
        return conn
    except RuntimeError as e:
        logger.error(
            f'database({conf.comment} was not opened. connection={conf.connect}')
        raise e


def open_postgresql(config: dict):
    conf = objdict(config)
    try:
        conn = psycopg2.connect(
            host=conf.host,
            port=conf.port,
            user=conf.user,
            password=conf.password,
            database=conf.database,
            options=f"-c search_path={conf.schema}")
        return conn
    except RuntimeError as e:
        logger.error(
            f'database({conf.comment} was not opened. connection={conf.connect}')
        raise e


def open_mysql(config: dict):
    conf = objdict(config)
    try:
        connect = MySQLdb.connect(
            host=conf.host,
            port=conf.port,
            user=conf.user,
            password=conf.password,
            db=conf.database,
            use_unicode=conf.use_unicode,
            charset=conf.charset
        )
        return connect
    except RuntimeError as e:
        logger.error(
            f'database({conf.comment} was not opened. connection={conf.connect}')
        raise e


def execute_sql_file(conn, sql_file: str):
    cursor = conn.cursor()
    logger.debug(f'read sql {sql_file}')
    with open(sql_file, 'r') as f:
        text = f.read()
        for sql in text.split(';'):
            sql = sql.strip()
            if len(sql) > 0:
                logger.debug(f'execute sql=\n{sql}')
                cursor.execute(sql)


reParam = re.compile(r"(\/\*(\w+)\*\/)(''|0|\(\))?")


def parse_2way_sql(sql: str, esc_char: str = '?') -> Iterable:
    '''
    2wayのSQLをパースし、/*パラメータ*/を?に入れ替え後、
    ？に入れ替わったパラメータリストを返却する
    '''

    paramInfo = reParam.findall(sql)
    # パラメータを？に変換
    newSql = reParam.sub(esc_char, sql)

    # 抽出したパラメータ名が、？の何番目かを返却する
    return (newSql, [name for (g1, name, g3) in paramInfo])


class DatabaseService(ServiceBase):
    def init(self, config: dict):
        self.__dbconfig = config

        # 設定されているDB情報をもとに接続を試してみる
        # 接続できなかったら例外をスローして終了
        logger.info("start db open check.")
        for db_name in self.__dbconfig:
            db_conf = objdict(self.__dbconfig[db_name])
            try:
                logger.info(f"try open '{db_name}'")
                with Closer(self.open(db_name)) as db:
                    if len(db_conf.init_sqls) > 0:
                        # sql一覧を取得
                        for sql_file in db_conf.init_sqls:
                            # SQLを実行(；区切りを順次実行)
                            execute_sql_file(db, sql_file)
                logger.info(f"ok '{db_name}'")
            except:
                logger.error(f"can't opened '{db_name}'")
                pass

    def start(self, context: ApplicationContext):
        # todo: コネクションプールの処理を行う
        pass

    def stop(self, context: ApplicationContext):
        # todo: コネクションプールで開いた接続を閉じる
        pass

    def open(self, db_name: str):
        if db_name in self.__dbconfig:
            db_conf = objdict(self.__dbconfig[db_name])
            db_type = db_conf.type
            if db_type == 'sqlite3':
                return open_sqlite(db_conf)
            if db_type == 'postgresql':
                return open_postgresql(db_conf)
            if db_type == 'mysql':
                return open_mysql(db_conf)
            else:
                logger.warn(f'{db_type} was not supported.')
        return None

    def cursor(self, db):
        if type(db) == psycopg2.extensions.connection:
            return db.cursor(cursor_factory=DictCursor)
        if type(db) == MySQLdb.connections.Connection:
            return db.cursor(MySQLdb.cursors.DictCursor)
        else:
            return db.cursor()

    def execute(self, cursor, sql: str, params: dict) -> Iterable:
        if sql.strip() == '':
            return []

        rep = "?"
        if type(cursor) in [psycopg2.extras.DictCursor, MySQLdb.cursors.DictCursor]:
            rep = '%s'

        (newSql, paramsIndex) = parse_2way_sql(sql, rep)

        if type(params) == Row:
            queryParams = [params.get(x) for x in paramsIndex]
        else:
            queryParams = [params[x] for x in paramsIndex]

        return cursor.execute(newSql, queryParams)

    def execute_query(self, cursor, sql: str, params: dict) -> Iterable:
        if sql.strip() == '':
            return []

        rep = "?"
        if type(cursor) in [psycopg2.extras.DictCursor, MySQLdb.cursors.DictCursor]:
            rep = '%s'

        (newSql, paramsIndex) = parse_2way_sql(sql, rep)

        if type(params) == Row:
            queryParams = [params.get(x) for x in paramsIndex]
        else:
            queryParams = [params[x] for x in paramsIndex]

        cursor.execute(newSql, queryParams)
        return CursorIterator(cursor)

    def execute_updates(self, cursor, sql: str, rows: list) -> Iterable:
        if sql.strip() == '':
            return []
        if len(rows) == 0:
            return []
        queryRows = []
        rep = '?'
        if type(cursor) in [psycopg2.extras.DictCursor, MySQLdb.cursors.DictCursor]:
            rep = '%s'

        (newSql, paramsIndex) = parse_2way_sql(sql, rep)
        for row in rows:
            if type(row) == Row:
                queryRows.append([row.get(x) for x in paramsIndex])
            else:
                queryRows.append([row[x] for x in paramsIndex])

        return cursor.executemany(newSql, queryRows)


def new_instance(loggerInject: Logger = None) -> ServiceBase:
    global logger
    logger = loggerInject
    return DatabaseService()
