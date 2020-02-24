import typing

from abc import ABCMeta, abstractmethod
from praqta.command_context import CommandContext


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
