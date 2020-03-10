import typing
from .. import CommandBase, IteratorCommandBase
from praqta.interface import Row, CommandContext, objdict

import csv
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class XsvReader(IteratorCommandBase):
    def __init__(self):
        super().__init__()
        self.__open_files = []

    def init(self, context: CommandContext):
        super().init(context)
        # パラメータ取得
        self.__params = context.get_parameters()
        super().set_fetch_size(self.__params.fetch_size)

    def get_new_data(self, parent_row):

        # ファイルオープン
        file = open(parent_row.get(self.__params.file_path_key),
                    encoding=self.__params.encoding
                    )
        # ファイルオブジェクトを保存(termでクローズ)
        self.__open_files.append(file)

        # 区切り文字を決定
        delimiter = ","
        if self.__params.delimiter == "tab":
            delimiter = "\t"
        if self.__params.delimiter == "semi":
            delimiter = ";"

        # CSV読み込みオブジェクトを設定(イテレータ)
        rows = csv.DictReader(
            file,
            delimiter=delimiter,
            doublequote=self.__params.doublequote,
            escapechar=self.__params.escape_char,
            quotechar=self.__params.quotechar
        )
        return iter(rows)

    def create_new_row(self, row):
        # 加工なし
        return row

    def term(self, context: CommandContext):
        # オープンしたファイルをクローズする
        for file in self.__open_files:
            file.close()


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return XsvReader()
