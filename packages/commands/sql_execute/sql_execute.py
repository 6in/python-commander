from .. import CommandBase
from logging import Logger
from praqta.interface import Row, CommandContext, objdict
from services.database.database import DatabaseService
from typing import cast
import services

logger = cast(Logger, {})


class SqlExecute(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        # パラメータを取得する
        self.__params = context.get_parameters()

        # データベースサービスを取得
        self.__dbService = cast(
            DatabaseService, services.get_service('database')[0])
        # アクセスしたいDB名を指定してDBインスタンスを取得
        logger.info(f"open database {self.__params.db_name}")
        self.__db = self.__dbService.open(self.__params.db_name)
        self.__cursor = self.__dbService.cursor(self.__db)

        # 事前の処理を実施
        for sql in self.__params.init_sql.split(";"):
            sql = sql.strip()
            self.__dbService.execute(
                self.__cursor, sql, context.get_script_parameters())

    def proc(self, context: CommandContext):
        rows = []

        sql = self.__params.main_sql

        # Rowラッパーに変換
        rows = []
        if self.__params.batch_count <= 0:
            # まとめてインサート
            rows = [Row(row) for row in context.get_rows()]
            if len(rows) > 0:
                self.__dbService.execute_updates(self.__cursor, sql, rows)
                self.__db.commit()
                logger.info(f"executed {len(rows)} parameters..")
        else:
            # 指定件数ずつまとめて実行
            insRows = []
            for row in context.get_rows():
                insRows.append(Row(row))
                if len(insRows) == self.__params.batch_count:
                    rows = rows + insRows
                    self.__dbService.execute_updates(
                        self.__cursor, sql, insRows)
                    logger.info(f"executed {len(insRows)} parameters.")
                    insRows = []

                    self.__db.commit()

            if len(insRows) > 0:
                rows = rows + insRows
                self.__dbService.execute_updates(
                    self.__cursor, sql, insRows)
                logger.info(f"executed {len(insRows)} parameters.")

        # 次のコマンドへ引渡し
        context.set_rows(rows)

    def term(self, context: CommandContext):
        # 事後のSQL処理を実行
        for sql in self.__params.term_sql.split(";"):
            sql = sql.strip()
            self.__dbService.execute(
                self.__cursor, sql, context.get_script_parameters())
        try:
            self.__cursor.close()
        except:
            pass
        logger.info(f"close database {self.__params.db_name}")

        self.__db.commit()
        self.__db.close()
        self.__db = None


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return SqlExecute()
