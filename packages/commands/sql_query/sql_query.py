import typing
from .. import CommandBase, IteratorCommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
from services.database.database import DatabaseService
import services

logger = cast(Logger, {})


class SqlQuery(IteratorCommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        super().__init__()

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        super().init(context)
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()
        # フェッチサイズを指定
        super().set_fetch_size(self.__params.fetch_size)

        # データベースサービスを取得
        self.__dbService = cast(
            DatabaseService, services.get_service('database')[0])
        # アクセスしたいDB名を指定してDBインスタンスを取得
        logger.info(f"open database {self.__params.db_name}")
        self.__db = self.__dbService.open(self.__params.db_name)
        self.__cursor = self.__dbService.cursor(self.__db)

    def get_new_data(self, parent_row):
        param = {}
        if self.__params.query_type == 'static':
            # スクリプトのpropertiesからパラメータを取得する
            for key in self.__params.query_parameters:
                param[key] = self.__params.get(key)
        else:
            # パラメータ値は、行データから取得
            for key in self.__params.query_parameters:
                param[key] = parent_row.get(key)

        # クエリを実行
        sql = self.__params.sql.format(**parent_row.raw())
        rows = self.__dbService.execute_query(
            self.__cursor, sql, param)

        return iter(rows)

    def create_new_row(self, row):
        return row

    def term(self, context: CommandContext):
        """
        カーソル、DBをクローズ
        """
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

    return SqlQuery()
