import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
import importlib

logger = cast(Logger, {})


class Script(CommandBase):
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

        modules = {}
        for key in self.__params.modules.keys():
            module_name = self.__params.modules[key]
            modules[key] = importlib.import_module(module_name)
        modules['objdict'] = objdict
        self.__modules = modules

        script = self.__params.script
        script = f'\n{script}\noutput_rows = proc(input_rows)'
        logger.debug(script)
        self.__script = script

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。
        """

        rows = []
        for row in context.get_rows():
            if type(row) == Row:
                rows.append(objdict(row.raw()))
            else:
                rows.append(objdict(row))

        local = {
            'input_rows': rows,
            'output_rows': []
        }

        # スクリプトの実行を行う
        try:
            exec(self.__script, self.__modules, local)
        except Exception as e:
            logger.error(e)
            raise e

        # 次のコマンドへ引渡し
        context.set_rows(local['output_rows'])

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

    return Script()
