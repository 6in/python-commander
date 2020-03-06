import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict

import csv
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class XsvReader(CommandBase):
    def __init__(self):
        self.__iter_parent_rows = None
        self.__open_files = []
        self.__has_parent_data = True
        self.__has_chidren_data = False

    def init(self, context: CommandContext):
        # パラメータ取得
        self.__params = context.get_parameters()

        # データ供給コマンドであることを設定
        context.set_supplier(self)

    def proc(self, context: CommandContext):
        # 親データを保存
        if self.__iter_parent_rows == None:
            self.__iter_parent_rows = iter([row for row in context.get_rows()])
            self.__has_parent_data = True

        # 親から１行取得し、オープンするべきファイルを取得する
        try:
            row = next(self.__iter_parent_rows)
        except StopIteration:
            self.__has_parent_data = False
            context.set_rows([])
            return

        # ファイルオープン
        file = open(row[self.__params.file_path_key],
                    encoding=self.__params.encoding)
        # ファイルオブジェクトを保存(termでクローズ)
        self.__open_files.append(file)

        # 区切り文字を決定
        delimiter = ","
        if self.__params.delimiter == "tab":
            delimiter = "\t"
        if self.__params.delimiter == "semi":
            delimiter = ";"

        # CSV読み込みオブジェクトを設定(イテレータ)
        context.set_rows(csv.DictReader(
            file,  delimiter=delimiter))

    def term(self, context: CommandContext):
        # オープンしたファイルをクローズする
        for file in self.__open_files:
            file.close()

    def has_data(self):
        return self.__has_parent_data or self.__has_chidren_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return XsvReader()
