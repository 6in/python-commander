import csv
import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class XsvWriter(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__has_data = True
        self.__headers = []
        self.__writer = None
        self.__write_header = False

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()

        # ファイルをオープンする
        logger.info(f"open file for csv write {self.__params.file_path}")
        self.__open_file = open(self.__params.file_path,
                                'w', encoding=self.__params.encoding)

        # 区切り文字を決定
        delimiter = ","
        if self.__params.delimiter == "tab":
            delimiter = "\t"
        if self.__params.delimiter == "semi":
            delimiter = ";"

        # 書き込みオブジェクトを作成
        self.__writer = csv.writer(
            self.__open_file,
            delimiter=delimiter,
            doublequote=self.__params.doublequote,
            escapechar=self.__params.escape_char,
            quotechar=self.__params.quotechar
        )
        self.__write_header = False

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。

        """

        # 次へ引き渡す行
        rows = []
        for row in iter(context.get_rows()):
            # Rowラッパーに変換
            row = Row(row)
            if self.__write_header == False:
                self.__write_header = True
                headers = self.__params.headers
                if len(self.__params.headers) == 0:
                    headers = row.keys()
                self.__headers = headers
                if self.__params.header:
                    self.__writer.writerow(headers)

            rows.append(row)
            # 行を追加
            self.__writer.writerow(
                [row.get(x) for x in self.__headers]
            )

        # 次のコマンドへ引渡し
        context.set_rows(rows)

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        self.__open_file.close()
        logger.info(f"close file {self.__params.file_path}")

    def has_data(self) -> bool:
        """
        このコマンドで提供できるデータが存在するかを返却
        CommandConext.set_supplierでセットしたコマンドだけが呼び出されます
        """
        return self.__has_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return XsvWriter()
