import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class Sample(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        context.set_supplier(self)
        self.__has_data = True
        self.__rows = [
            Row({'p1': 'abc', 'p2': 123, 'p3': True}),
            Row({'p1': 'def', 'p2': 456, 'p3': False}),
            Row({'p1': 'ghi', 'p2': 789, 'p3': True}),
            Row({'p1': 'abc', 'p2': 123, 'p3': True}),
        ]

    def proc(self, context: CommandContext):
        rows = self.__rows
        context.set_rows(iter(rows))
        self.__has_data = False

    def term(self, context: CommandContext):
        pass

    def has_data(self):
        return self.__has_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return Sample()
