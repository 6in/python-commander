import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
from services.database.database import DatabaseService
import services

logger = cast(Logger, {})


class SqlQuery(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__has_data = True
        self.__iter_parent = None
        self.__has_parent_data = True
        self.__iter_current = None
        self.__has_current_data = True

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()
        # このコマンドがデータを供給するならコメントアウト
        context.set_supplier(self)

        # データベースサービスを取得
        self.__dbService = cast(
            DatabaseService, services.get_service('database')[0])
        # アクセスしたいDB名を指定してDBインスタンスを取得
        logger.info(f"open database {self.__params.db_name}")
        self.__db = self.__dbService.open(self.__params.db_name)
        self.__cursor = self.__dbService.cursor(self.__db)

    def proc(self, context: CommandContext):
        """
        クエリを実行する。
        実行パターンは2つ。
            上位の行データの値をクエリパラメータとして、SQL発行するタイプ
        """

        if self.__params.query_type == 'static':
            # 親データの参照はしないので、データなしに設定
            self.__has_parent_data = False

            if self.__iter_current == None:
                # パラメータ組み立て
                param = {}
                for key in self.__params.query_parameters:
                    param[key] = self.__params.get(key)

                # クエリを実行
                rows = self.__dbService.execute_query(
                    self.__cursor, self.__params.sql, param)
                logger.info(
                    f"execute static query \n{self.__params.sql}: {param}")

                if self.__params.fetch_size <= 0:
                    # フェッチ件数指定がないなら、抽出結果を設定する
                    context.set_rows(rows)
                    self.__has_current_data = False
                    return
                else:
                    # イテレータを保存
                    self.__iter_current = iter(rows)

        # 動的SQL実行
        if self.__params.query_type == 'dynamic':
            row = {}
            if self.__iter_parent == None:
                # 入力データを保存
                self.__iter_parent = iter([row for row in context.get_rows()])
                pass

            if self.__iter_current == None:
                # 保存済みのデータから１行フェッチ
                try:
                    row = next(self.__iter_parent)
                except StopIteration:
                    self.__has_parent_data = False
                    self.__iter_parent = None
                    context.set_rows([])
                    return

            # SQLを実行する
            if self.__iter_current == None:
                param = {}
                for key in self.__params.query_parameters:
                    # パラメータ値は、行データから取得
                    param[key] = row[key]

                # クエリ実行
                rows = self.__dbService.execute_query(
                    self.__cursor, self.__params.sql, param)
                logger.info(
                    f"execute dynamic query \n{self.__params.sql}: {param}")

                if self.__params.fetch_size <= 0:
                    # 全行を返却する場合は、現在のデータ提供は終了
                    context.set_rows(rows)
                    self.__has_current_data = False
                    return
                else:
                    self.__iter_current = iter(rows)

        # ここまで来たのは、fetch_size > 0の場合
        retRows = []
        while True:
            try:
                row = next(self.__iter_current)
            except StopIteration:
                self.__iter_current = None
                self.__has_current_data = False
                break

            retRows.append(row)

            # フェッチサイズに達したらwhileループ終了
            if len(retRows) == self.__params.fetch_size:
                break

        # データを設定
        context.set_rows(retRows)

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

    def has_data(self) -> bool:
        """
        データの有無を返却
        """
        return self.__has_parent_data or self.__has_current_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return SqlQuery()
