from .. import CommandBase, IteratorCommandBase
from datetime import datetime
from glob import iglob
from logging import Logger
from praqta.interface import Row, CommandContext, objdict
from typing import cast
import hashlib
import os
import os.path
import re
import typing
from chardet.universaldetector import UniversalDetector

logger = cast(Logger, {})


class RowIterator(object):
    '''
    行返却用イテレータ。利用しない場合は削除してください。
    '''

    def __init__(self, rows, params):
        '''
        コンストラクタ        
        '''
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
            file = next(self.__rows)
        except StopIteration as e:
            raise e

        path = os.path.abspath(file)
        (parent, name) = os.path.split(path)

        # 行データ返却
        row['parent'] = parent
        row['path'] = path
        row['name'] = name

        return row


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


class FileList(IteratorCommandBase):
    def __init__(self):
        '''
        コンストラクタ
        メンバー変数の初期化をここで行います。
        '''
        super().__init__()

    def init(self, context: CommandContext):
        '''
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        '''
        super().init(context)
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()
        # フェッチサイズを指定
        super().set_fetch_size(self.__params.fetch_size)

        self.__white_filters = [re.compile(x)
                                for x in self.__params.white_list]

        self.__black_filters = [re.compile(x)
                                for x in self.__params.black_list]

        self.__detector = UniversalDetector()

    def get_encode(self, path: str) -> str:
        self.__detector.reset()
        with open(path, 'rb') as f:
            for line in f.readlines():
                self.__detector.feed(line)
                if self.__detector.done:
                    break
            self.__detector.close()
            return self.__detector.result['encoding']

    def get_new_data(self, parent_row):
        # 検索開始
        file_search_key = self.__params.file_search_key
        search_path = parent_row.get(file_search_key)

        # 検索対象取得
        search_target = self.__params.search_target
        if search_target == 'folder':
            search_path = f'{search_path}{os.sep}**{os.sep}'
        else:
            search_path = f'{search_path}{os.sep}**'

        self.__is_file_only = search_target == 'file'

        return RowIterator(iglob(search_path, recursive=self.__params.recursive), self.__params)

    def create_new_row(self, row):
        newRow = {}
        path = row['path']
        parent = row['parent']

        name = row['name']

        # パターンチェック
        # logger.debug(path)
        if len(self.__white_filters) > 0 and len([name for reg in self.__white_filters if len(reg.findall(name)) > 0]) == 0:
            return None

        if len(self.__black_filters) > 0 and len([name for reg in self.__black_filters if len(reg.findall(name)) > 0]) > 0:
            return None

        is_file = os.path.isfile(path)

        # ファイルのみの場合は、ファイルでないものはスキップ
        if self.__is_file_only == True and is_file == False:
            return None

        length = 0
        if is_file and 'length' in self.__params.attributes:
            length = os.path.getsize(path)

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

        md5 = ''
        if is_file and 'md5' in self.__params.attributes:
            md5 = get_md5(path)

        encoding = ''
        if is_file and 'encoding' in self.__params.attributes:
            encoding = self.get_encode(path)

        localRow = {
            'path': path,
            'parent': parent,
            'name': name,
            'is_file': is_file,
            'ext': ext,
            'length': length,
            'create_date': create_date,
            'update_date': update_date,
            'md5': md5,
            'encoding': encoding,
        }

        newRow = {}
        for key in self.__params.attributes:
            newRow[key] = localRow[key]

        return newRow

    def term(self, context: CommandContext):
        '''
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        '''
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return FileList()
