from praqta import CommandBase
import importlib
import os
import os.path
import typing
import yaml
import time


class ModuleInfo(object):

    def __init__(self, name, module):
        self.__module = module
        self.__file = module.__file__
        self.__timestamp = os.stat(self.__file).st_mtime
        self.load_spec()

    def load_spec(self):
        # Yamlファイルをロード
        (path, _) = os.path.splitext(self.__file)
        with open(f'{path}.yml', 'r') as f:
            self.__spec = yaml.load(f)
            print(self.__spec)
            # todo: json schemaによるspecのチェック

    def get_spec(self) -> dict:
        return self.__spec

    def is_updated(self):
        return os.stat(self.__file).st_mtime > self.__timestamp

    def get_module(self):
        return self.__module

    def reload(self):
        importlib.reload(self.__module)
        return self

    def new_instance(self):
        return self.__module.new_instance()


# モジュールのキャッシュ
__moduleInfoCache = {}


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
