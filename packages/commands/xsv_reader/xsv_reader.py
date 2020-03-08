import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict

import csv
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class XsvReader(CommandBase):
    def __init__(self):
        self.__iter_parent = None
        self.__iter_curent = None
        self.__has_parent_data = True
        self.__has_current_data = True
        self.__open_files = []

    def init(self, context: CommandContext):
        # パラメータ取得
        self.__params = context.get_parameters()

        # データ供給コマンドであることを設定
        context.set_supplier(self)

    def proc(self, context: CommandContext):
        # 親データを保存
        if self.__iter_parent == None:
            self.__iter_parent = iter([Row(row) for row in context.get_rows()])
            self.__has_parent_data = True

        # 親から１行取得し、オープンするべきファイルを取得する
        if self.__iter_curent == None:
            try:
                row = next(self.__iter_parent)
            except StopIteration:
                self.__has_parent_data = False
                self.__iter_parent = None
                context.set_rows([])
                return

        if self.__iter_curent == None:

            # ファイルオープン
            file = open(row.get(self.__params.file_path_key),
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
        # オープンしたファイルをクローズする
        for file in self.__open_files:
            file.close()

    def has_data(self):
        return self.__has_parent_data or self.__has_current_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return XsvReader()
