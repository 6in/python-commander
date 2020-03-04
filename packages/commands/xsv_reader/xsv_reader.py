import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict

import csv


class XsvReader(CommandBase):
    def __init__(self):
        self.__iter_rows = None
        self.__open_files = []

    def init(self, context: CommandContext):
        self.__params = objdict(context.get_parameters())

    def proc(self, context: CommandContext):
        # 最初に取得したデータを保存
        if self.__iter_rows == None:
            self.__iter_rows = iter([row for row in context.get_rows()])

        # 保存したデータから１行取得
        try:
            row = next(self.__iter_rows)
        except StopIteration:
            context.set_rows([])
            return

        # ファイルオープン
        file = open(row[self.__params.file_path_key],
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
        context.set_rows(csv.DictReader(
            file,  delimiter=delimiter))

    def term(self, context: CommandContext):
        # オープンしたファイルをクローズする
        for file in self.__open_files:
            file.close()


def new_instance() -> CommandBase:
    return XsvReader()
