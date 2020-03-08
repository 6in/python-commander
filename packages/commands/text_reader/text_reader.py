import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
import os

logger = cast(Logger, {})


class TextReader(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__iter_parent = None
        self.__iter_curent = None
        self.__has_parent_data = True
        self.__has_current_data = False

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

    def proc(self, context: CommandContext):
        """
        ファイルをオープンし、全行データを後続に流します。
        """

        # 親データを保存
        if self.__iter_parent == None:
            self.__iter_parent = iter([Row(row) for row in context.get_rows()])
            self.__has_parent_data = True

        # 親から１行取得し、オープンするべきファイルを取得する
        if self.__iter_curent == None:
            try:
                parent_row = next(self.__iter_parent)
            except StopIteration:
                self.__has_parent_data = False
                self.__iter_parent = None
                context.set_rows([])
                return

        if self.__iter_curent == None:

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
                context.set_rows([])
                return

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

            context.set_rows(rows)

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass

    def has_data(self) -> bool:
        """
        このコマンドで提供できるデータが存在するかを返却
        CommandConext.set_supplierでセットしたコマンドだけが呼び出されます
        """
        return self.__has_parent_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return TextReader()
