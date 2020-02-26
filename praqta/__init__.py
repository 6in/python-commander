
import typing
from praqta.command_context import CommandContext
from abc import ABCMeta, abstractmethod


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
