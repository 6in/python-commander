import typing
from .. import CommandBase, IteratorCommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class RowIterator(object):
    """
    行返却用イテレータ。利用しない場合は削除してください。
    """

    def __init__(self, rows, params):
        """
        コンストラクタ        
        """
        self.__params = params
        if type(rows) == list:
            self.__rows = iter(rows)
        else:
            self.__rows = rows

    def __iter__(self):
        return self

    def __next__(self):
        row = {}
        # データ取得処理
        try:
            row = next(self.__rows)
        except StopIteration as e:
            raise e

        # 行データを加工する処理

        # 行データ返却
        return dict(row)


class Template(IteratorCommandBase):
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
        # 親クラス呼出
        super().init(context)

        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()

        # フェッチサイズを指定
        super().set_fetch_size(0)

    def get_new_data(self, parent_row):
        """
        コマンドが返却するデータを取得する処理
        """
        return []

    def create_new_row(self, row):
        """
        データ加工処理
        """
        return dict(row)

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return Template()
