import hashlib
import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
from glob import glob
import os
import os.path
import re
from datetime import datetime

logger = cast(Logger, {})


def get_md5(path: str) -> str:

    # ハッシュアルゴリズムを決めます
    algo = 'md5'

    # ハッシュオブジェクトを作ります
    h = hashlib.new(algo)

    # 分割する長さをブロックサイズの整数倍に決めます
    Length = hashlib.new(algo).block_size * 0x800

    with open(path, 'rb') as f:
        BinaryData = f.read(Length)

        # データがなくなるまでループします
        while BinaryData:

            # ハッシュオブジェクトに追加して計算します。
            h.update(BinaryData)

            # データの続きを読み込む
            BinaryData = f.read(Length)

    return h.hexdigest()


class FileList(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__iter_parent = None
        self.__iter_current = None
        self.__has_parent_data = True
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

        self.__white_filters = [re.compile(x)
                                for x in self.__params.white_list]

        self.__black_filters = [re.compile(x)
                                for x in self.__params.black_list]

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。

        """

        # 親データを保存
        if self.__iter_parent == None:
            self.__iter_parent = iter([row for row in context.get_rows()])
            self.__has_parent_data = True

        # 親から１行取得し、オープンするべきファイルを取得する
        if self.__iter_current == None:
            try:
                row = Row(next(self.__iter_parent))
            except StopIteration:
                self.__has_parent_data = False
                self.__iter_parent = None
                context.set_rows([])
                return

        if self.__iter_current == None:

            # 検索開始
            file_search_key = self.__params.file_search_key
            search_path = row.get(file_search_key)

            # 検索対象取得
            search_target = self.__params.search_target
            if search_target == 'folder':
                search_path = f"{search_path}{os.sep}**{os.sep}"
            else:
                search_path = f"{search_path}{os.sep}**"

            is_file_only = search_target == 'file'

            newRows = []
            for file in glob(search_path, recursive=self.__params.recursive):
                path = os.path.abspath(file)
                (parent, name) = os.path.split(path)

                # パターンチェック
                # logger.debug(path)
                if len(self.__white_filters) > 0 and len([name for reg in self.__white_filters if len(reg.findall(name)) > 0]) == 0:
                    continue

                if len(self.__black_filters) > 0 and len([name for reg in self.__black_filters if len(reg.findall(name)) > 0]) > 0:
                    continue

                is_file = os.path.isfile(path)

                # ファイルのみの場合は、ファイルでないものはスキップ
                if is_file_only == True and is_file == False:
                    continue

                length = 0
                if is_file and 'length' in self.__params.attributes:
                    length = os.path.getsize(file)

                (_, ext) = os.path.splitext(path)

                create_date = ''
                update_date = ''
                stat = os.stat(path)

                if 'create_date' in self.__params.attributes:
                    create_date = datetime.fromtimestamp(stat.st_ctime).strftime(
                        '%Y-%m-%d %H:%M:%S')

                if 'update_date' in self.__params.attributes:
                    update_date = datetime.fromtimestamp(stat.st_mtime).strftime(
                        '%Y-%m-%d %H:%M:%S')

                if len(ext) > 0:
                    ext = ext[1:].lower()

                md5 = ""
                if "md5" in self.__params.attributes:
                    md5 = get_md5(path)

                localRow = {
                    "path": path,
                    "parent": parent,
                    "name": name,
                    "is_file": is_file,
                    "ext": ext,
                    "length": length,
                    "create_date": create_date,
                    "update_date": update_date,
                    "md5": md5
                }

                newRow = {}
                for key in self.__params.attributes:
                    newRow[key] = localRow[key]

                newRows.append(newRow)

            context.set_rows(newRows)
            self.__has_current_data = False

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass

    def has_data(self):
        return self.__has_parent_data or self.__has_current_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return FileList()
