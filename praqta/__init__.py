
from abc import ABCMeta, abstractmethod
# from praqta import CommandBase
from praqta.command_context import CommandContext
import importlib
import os
import os.path
import time
import typing
import typing
import yaml


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


class Row(object):
    def __init__(self, row: dict):
        self.__row = row

    def __getitem__(self, name: str):

        if name in self.__row:
            return self.__row[name]
        else:
            return None


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


class ApplicationContext(object):
    def __init__(self):
        pass

    def get_config(self, section: str) -> dict:
        return {}
