from .. import ServiceBase
from praqta.interface import ApplicationContext, objdict
from typing import Iterable
import sqlite3
import re


def open_sqlite(config: dict) -> sqlite3.Connection:
    conf = objdict(config)
    try:
        conn = sqlite3.connect(conf.connect)
        conn.row_factory = sqlite3.Row
        return conn
    except RuntimeError as e:
        print(
            f'database({conf.comment} was not opened. connection={conf.connect}')
        raise e


def execute_sql_file(conn, sql_file: str):
    cursor = conn.cursor()
    print(f'read sql {sql_file}')
    with open(sql_file, 'r') as f:
        text = f.read()
        for sql in text.split(';'):
            sql = sql.strip()
            if len(sql) > 0:
                print(f'execute sql=\n{sql}')
                cursor.execute(sql)


reParam = re.compile(r"(\/\*(\w+)\*\/)(''|0|\(\))?")


def parse_2way_sql(sql: str) -> Iterable:
    '''
    2wayのSQLをパースし、/*パラメータ*/を?に入れ替え後、
    ？に入れ替わったパラメータリストを返却する
    '''

    paramInfo = reParam.findall(sql)
    # パラメータを？に変換
    newSql = reParam.sub('?', sql)

    # 抽出したパラメータ名が、？の何番目かを返却する
    return (newSql, [name for (g1, name, g3) in paramInfo])


class DatabaseService(ServiceBase):
    def init(self, config: dict):
        self.__dbconfig = config
        print(f'DatabaseService.init({config})')

        # 設定されているDB情報をもとに接続を試してみる
        # 接続できなかったら例外をスローして終了
        for db_name in self.__dbconfig:
            db_conf = objdict(self.__dbconfig[db_name])
            with self.open(db_name) as db:
                if len(db_conf.init_sqls) > 0:
                    # sql一覧を取得
                    for sql_file in db_conf.init_sqls:
                        # SQLを実行(；区切りを順次実行)
                        execute_sql_file(db, sql_file)

    def start(self, context: ApplicationContext):
        # todo: コネクションプールの処理を行う
        pass

    def stop(self, context: ApplicationContext):
        # todo: コネクションプールで開いた接続を閉じる
        pass

    def open(self, db_name: str):
        for db_name in self.__dbconfig:
            db_conf = objdict(self.__dbconfig[db_name])
            db_type = db_conf.type
            if db_type == 'sqlite3':
                return open_sqlite(db_conf)
            else:
                print(f'{db_type} was not supported.')
        return None

    def execute_query(self, cursor, sql: str, params: dict) -> Iterable:
        if sql.strip() == '':
            return []
        (newSql, paramsIndex) = parse_2way_sql(sql)
        queryParams = [params[x] for x in paramsIndex]
        return cursor.execute(newSql, queryParams)

    def execute_queries(self, cursor, sql: str, rows: list) -> Iterable:
        if sql.strip() == '':
            return []
        if len(rows) == 0:
            return []
        (newSql, paramsIndex) = parse_2way_sql(sql)

        queryRows = []
        for row in rows:
            queryRows.append([row[x] for x in paramsIndex])
        # print(f"{newSql} param => {queryParams}")
        return cursor.executemany(newSql, queryRows)


def new_instance() -> ServiceBase:
    return DatabaseService()
