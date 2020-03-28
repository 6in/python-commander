import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
from jinja2 import Template

logger = cast(Logger, {})


class TemplateWriter(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__has_data = True

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()
        # このコマンドがデータを供給するならコメントアウト
        # context.set_supplier(self)
        self.__template = Template(self.__params.template)

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。

        """

        # 次へ引き渡す行
        rows = [row for row in context.get_rows()]
        if len(rows) == 0:
            return rows

        if type(rows[0]) == Row:
            rows = [row.raw() for row in rows]

        output_path = self.__params.output.format(**rows[0])

        # テンプレートを適用
        result = self.__template.render(rows=rows, args=self.__params.args)
        with open(output_path, 'w') as f:
            f.write(result)

        # 次のコマンドへ引渡し
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
        return self.__has_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return TemplateWriter()
