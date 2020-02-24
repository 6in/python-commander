import typing
from commands.command_base import CommandBase
import commands.sample.command
import importlib
import yaml
import os.path

# モジュールのキャッシュ
__command_module_cache = {}
__command_specs = {}


def load_spec(key: str, path: str):
    with open(path, 'r') as f:
        __command_specs[key] = yaml.load(f)


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

    if key in __command_module_cache:
        # キャッシュからモジュールを取得
        module = __command_module_cache[key]
        print("get module from cache.")
    else:
        # モジュールを動的にロード
        module = importlib.import_module(key)
        __command_module_cache[key] = module
        (path, ext) = os.path.splitext(module.__file__)
        path + ".py"

    return module.new_instance()
