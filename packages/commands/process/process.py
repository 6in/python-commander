import typing
from .. import CommandBase, IteratorCommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
import subprocess
import re
from datetime import datetime

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
            line = next(self.__rows)
        except StopIteration as e:
            raise e

        # 行データ返却
        row['stdout'] = line.rstrip().decode('utf8')

        return row


class Process(IteratorCommandBase):
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
        super().set_fetch_size(self.__params.fetch_size)

        self.__reg_split = re.compile(self.__params.split_reg)

    def get_new_data(self, parent_row):
        """
        コマンドが返却するデータを取得する処理
        """

        self.__parent_row = dict(parent_row.raw())

        # コマンドラインを取得
        command_line = self.__params.command_line
        command_line = command_line.format(**parent_row.raw())
        working_dir = self.__params.working_folder.format(**parent_row.raw())

        # ここでプロセスが (非同期に) 開始する.
        self.__proc = subprocess.Popen(
            command_line,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=working_dir)

        return RowIterator(iter(self.__proc.stdout.readline, b''), self.__params)

    def create_new_row(self, row):
        """
        データ加工処理
        """
        line = row['stdout']
        if self.__params.split:
            i = 1
            prefix = self.__params.column_name
            for work in self.__reg_split.split(line):
                key = f'{prefix}{i}'
                row[key] = work
                i += 1

        if self.__params.timestamp:
            row['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        parent_row = dict(self.__parent_row)
        for key in row.keys():
            parent_row[key] = row[key]
        return parent_row

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return Process()
