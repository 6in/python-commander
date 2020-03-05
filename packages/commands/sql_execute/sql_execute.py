from typing import cast
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
import services
from services.database.database import DatabaseService


class SqlExecute(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        # パラメータを取得する
        self.__params = objdict(context.get_parameters())

        # データベースサービスを取得
        self.__dbService = cast(
            DatabaseService, services.get_service('database')[0])
        # アクセスしたいDB名を指定してDBインスタンスを取得
        self.__db = self.__dbService.open(self.__params.db_name)
        self.__cursor = self.__db.cursor()

        # 事前の処理を実施
        for sql in self.__params.init_sql.split(";"):
            sql = sql.strip()
            self.__dbService.execute_query(
                self.__cursor, sql, context.get_script_parameters())

    def proc(self, context: CommandContext):
        rows = []
        sql = self.__params.main_sql

        # Rowラッパーに変換
        rows = []
        if self.__params.batch_count <= 0:
            # まとめてインサート
            rows = [Row(row) for row in context.get_rows()]
            self.__dbService.execute_queries(self.__cursor, sql, rows)
        else:
            # 指定件数ずつまとめてインサート
            insRows = []
            for row in context.get_rows():
                insRows.append(Row(row))
                if len(insRows) == self.__params.batch_count:
                    rows = rows + insRows
                    self.__dbService.execute_queries(
                        self.__cursor, sql, insRows)
                    insRows = []
                    self.__db.commit()

            rows = rows + insRows
            self.__dbService.execute_queries(
                self.__cursor, sql, insRows)

        # 次のコマンドへ引渡し
        context.set_rows(rows)

    def term(self, context: CommandContext):

        for sql in self.__params.term_sql.split(";"):
            sql = sql.strip()
            self.__dbService.execute_query(
                self.__cursor, sql, context.get_script_parameters())

        try:
            self.__cursor.close()
        except:
            pass

        self.__db.commit()
        self.__db.close()

        self.__db = None


def new_instance() -> CommandBase:
    return SqlExecute()
