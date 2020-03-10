import typing
from .. import CommandBase, IteratorCommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
import os

logger = cast(Logger, {})


class TextReader(IteratorCommandBase):
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
        super().set_fetch_size(self.__params.fetch_size)

    def get_new_data(self, parent_row):

        # ファイルパスを取得
        file_path = parent_row.get(self.__params.file_path_key)
        file_path = os.path.abspath(file_path)

        # タブ変換サイズの取得
        tab_size = 8
        if self.__params.untabify:
            (_, ext) = os.path.splitext(file_path)
            exts = objdict(self.__params.untabify_ext)
            if ext in exts:
                tab_size = exts[ext]

        # ファイルオープン
        logger.info(f"open file {file_path}")
        if os.path.exists(file_path) == False:
            logger.error(f'file is not exists. => {file_path}')
            return []

        # ファイルオープン
        with open(file_path, 'r', encoding=self.__params.encoding) as f:
            lines = f.readlines()
            rows = []
            line_no = 0
            for line in lines:
                line_no += 1
                # 右側の空白は除去
                line = line.rstrip()
                # 空チェック
                is_empty = line.strip() == ''
                # タブサイズ変換
                if self.__params.untabify:
                    line = line.expandtabs(tab_size)
                # 行オブジェクト生成
                row = {
                    'file_path': file_path,
                    'line_no': line_no,
                    'is_empty': is_empty,
                    'line': line
                }
                # 空行スキップ判定
                if self.__params.skip_empty and is_empty:
                    continue
                # 親データをコピー
                newRow = dict(parent_row.raw())
                # 指定属性のみコピーする
                for key in self.__params.attributes:
                    newRow[key] = row[key]
                # 行を追加
                rows.append(newRow)
        return iter(rows)

    def create_new_row(self, row):
        return row

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return TextReader()
