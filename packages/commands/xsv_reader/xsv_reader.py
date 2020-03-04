import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict

import csv


def is_place_holder(key: str) -> bool:
    return key[0] == '{'


def get_place_holder_key(key: str) -> str:
    if is_place_holder(key):
        key = key[1:-1]
    return key


def get_value(row: Row, key: str) -> str:
    pass


class XsvReader(CommandBase):
    def __init__(self):
        self.__save_rows = None
        self.__open_files = []
        self.__cur_file = None
        self.__cur_line = None
        self.__cur_file = None

    def init(self, context: CommandContext):
        self.__props = objdict(context.get_args())

    def proc(self, context: CommandContext):
        # 最初に取得したデータを保存
        if self.__save_rows == None:
            self.__save_rows = [row for row in context.get_rows()]

            if len(self.__save_rows) == 0:
                return

            # 保存行を１行取り出し
            row = self.__save_rows[0]
            self.__save_rows = self.__save_rows[1:]

            # ファイルオープン
            file = open(row[self.__props.file_path_key], 'r')
            self.__open_files.append(file)

            # CSV読み込みオブジェクトを返却
            context.set_rows(csv.DictReader(file, delimitor=","))

    def term(self, context: CommandContext):
        for file in self.__open_files:
            file.close()


def new_instance() -> CommandBase:
    return XsvReader()
