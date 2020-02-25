from commands.command_base import CommandBase
import commands.sample.command
import importlib
import os
import os.path
import typing
import yaml
import time


class ModuleInfo(object):

    def __init__(self, name, module):
        self.__module = module
        file = module.__file__
        (path, _) = os.path.splitext(file)
        with open(path + '.yml', 'r') as f:
            self.__spec = yaml.load(f)
        self.__file = file
        self.__timestamp = os.stat(self.__file).st_mtime

    def is_updated(self):
        return os.stat(self.__file).st_mtime > self.__timestamp

    def get_module(self):
        return self.__module


# モジュールのキャッシュ
__command_module_cache = {}


def create_command(command_name: str) -> CommandBase:
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
    key = f'commands.{command_name}.command'
    need_load = True
    if key in __command_module_cache:
        # キャッシュからモジュールを取得
        module = __command_module_cache[key]
        need_load = False
        # モジュールのタイムスタンプが新しくなっていたら、モジュール再ロード
        if module.is_updated():
            need_load = True

    if need_load:
        # モジュールを動的にロード
        module = ModuleInfo(command_name,
                            importlib.import_module(key))
        # キャッシュに格納
        __command_module_cache[key] = module

    return module.get_module() .new_instance()
