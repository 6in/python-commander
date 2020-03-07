import typing
from .. import CommandBase
from praqta.interface import CommandContext, Row
from typing import cast
from logging import Logger

logger = cast(Logger, {})


class Echo(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        self.__args = context.get_parameters()

    def proc(self, context: CommandContext):
        step = context.get_step()
        targets = self.__args.target_keys
        print('================================')
        newRows = []
        for row in context.get_rows():
            newRow = Row(row)
            newRows.append(newRow)
            for target in targets:
                value = newRow.get(target)
                print(f'echo {step}:{target}={value}')
            print('----------------------------')
        context.set_rows(newRows)

    def term(self, context: CommandContext):
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return Echo()
