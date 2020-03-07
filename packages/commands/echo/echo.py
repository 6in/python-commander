import typing
from .. import CommandBase
from praqta.interface import CommandContext, Row
from typing import cast
from logging import Logger

import prettytable

logger = cast(Logger, {})


class Echo(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        self.__args = context.get_parameters()

    def proc(self, context: CommandContext):
        targets = self.__args.target_keys

        newRows = [Row(row) for row in context.get_rows()]
        if len(newRows) == 0:
            return

        if len(targets) == 0:
            targets = newRows[0].keys()

        table = prettytable.PrettyTable(targets)

        # アラインの設定
        for key in targets:
            val = newRows[0].get(key)
            table.align[key] = 'l'
            if type(val) == int:
                table.align[key] = 'r'
            if type(val) == bool:
                table.align[key] = 'c'

        for row in newRows:
            table.add_row(
                [row.get(target) for target in targets]
            )

        print(table)
        context.set_rows(newRows)

    def term(self, context: CommandContext):
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return Echo()
