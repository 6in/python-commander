from abc import ABCMeta, abstractmethod
from praqta.interface import ModuleInfo, CommandContext
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


def get_command_arg_spec(command_name: str) -> dict:
    """
    コマンドの引数の仕様を返却
    """
    packageName = f'commands.{command_name}.{command_name}'
    return __moduleInfoCache[packageName].get_spec()


def new_instance(command_name: str) -> CommandBase:
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

    return moduleInfo.new_instance()
