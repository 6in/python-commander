from abc import ABCMeta, abstractmethod
from praqta.interface import ModuleInfo, CommandContext, Row
import importlib
import os
import os.path
import time
import typing
import yaml

# モジュールのキャッシュ
__moduleInfoCache = {}


class CommandBase(metaclass=ABCMeta):
    @abstractmethod
    def init(self, context: CommandContext):
        pass

    @abstractmethod
    def proc(self, context: CommandContext):
        pass

    @abstractmethod
    def term(self, context: CommandContext):
        pass


class IteratorCommandBase(CommandBase, metaclass=ABCMeta):
    """
    動的なデータ提供を行うコマンドの基本クラス
    親データの行の内容をパラメータとして、新たにデータを取得するような処理を行う
    場合は、このクラスから継承すると、以下の2つのメソッドを定義することで、
    * get_new_rows()
    * create_new_row()
    簡単に動的データ提供処理を作成することができます。
    """

    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__iter_parent = None
        self.__iter_current = None
        self.__has_parent_data = True
        self.__has_current_data = True
        # このコマンドで提供するデータの返却件数を指定。0以下なら全行提供する
        self.__fetch_size = 0
        self.__parent_row = {}

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        # このコマンドがデータを供給する宣言
        context.set_supplier(self)
        # フェッチサイズの指定
        self.set_fetch_size(0)

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。s
        """

        # 親データを保存
        if self.__iter_parent == None:
            self.__iter_parent = iter([row for row in context.get_rows()])
            self.__has_parent_data = True

        # 親から１行取得する
        if self.__iter_current == None:
            try:
                self.__parent_row = Row(next(self.__iter_parent))
            except StopIteration:
                self.__has_parent_data = False
                self.__iter_parent = None
                context.set_rows([])
                return

        if self.__iter_current == None:
            # このコマンドが提供するデータの取得処理を行う。
            # 例）ファイルをオープンして、データを読み込む

            # データ取得処理
            newRows = []
            newRows = self.get_new_data(self.__parent_row)

            # 取得したデータを、未加工のまま次の処理へ
            self.__iter_current = iter(newRows)

        retRows = []
        while True:
            try:
                row = next(self.__iter_current)
            except StopIteration:
                self.__iter_current = None
                self.__has_current_data = False
                break

            # 返却データを追加
            retRows.append(self.create_new_row(row))

            # フェッチサイズに達したらwhileループ終了
            if self.__fetch_size > 0 and len(retRows) == self.__fetch_size:
                break

        # データを設定
        context.set_rows(retRows)

    def set_fetch_size(self, fetch_size):
        self.__fetch_size = fetch_size

    def get_fetch_size(self):
        return self.__fetch_size

    @abstractmethod
    def get_new_data(self, parent_row):
        """
        親データのレコードをパラメータとして、コマンドで返却するデータを返却する
        配列あるいは、イテレータで返却する
        """
        pass

    @abstractmethod
    def create_new_row(self, row):
        """
        取得したデータの加工処理を行います
        """
        pass

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass

    def has_data(self) -> bool:
        """
        このコマンドで提供できるデータが存在するかを返却
        """
        return self.__has_parent_data or self.__has_current_data


def get_command_arg_spec(command_name: str) -> dict:
    """
    コマンドの引数の仕様を返却
    """
    packageName = f'commands.{command_name}.{command_name}'
    return __moduleInfoCache[packageName].get_spec()


def new_instance(command_name: str, logger) -> CommandBase:
    """
    コマンドのインスタンスを返却します

    Parameters
    ----------
    command_name : str
        コマンド名

    Returns
    -------
    commandInstance : CommandBase
    """
    packageName = f'commands.{command_name}.{command_name}'
    need_load = True
    if packageName in __moduleInfoCache:
        # キャッシュからモジュールを取得
        moduleInfo = __moduleInfoCache[packageName]
        need_load = False
        # モジュールのタイムスタンプが新しくなっていたら、モジュール再ロード
        if moduleInfo.is_updated():
            moduleInfo.reload()

    if need_load:
        # モジュールを動的にロード
        moduleInfo = ModuleInfo(command_name,
                                importlib.import_module(packageName))
        # キャッシュに格納
        __moduleInfoCache[packageName] = moduleInfo

    return moduleInfo.new_instance(logger)
