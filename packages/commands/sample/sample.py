import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext


class Sample(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        self.__rows = [
            Row({'p1': 'abc', 'p2': 123, 'p3': True}),
            Row({'p1': 'def', 'p2': 456, 'p3': False}),
            Row({'p1': 'ghi', 'p2': 789, 'p3': True}),
            Row({'p1': 'abc', 'p2': 123, 'p3': True}),
        ]

    def proc(self, context: CommandContext):
        rows = self.__rows
        print(f"proc: step={context.get_step()}")
        if len(rows) == 0:
            context.set_stop()
        else:
            # row = self.__rows[:1]
            # self.__rows = self.__rows[1:]
            context.set_rows(rows)
            context.set_stop()

    def term(self, context: CommandContext):
        pass


def new_instance() -> CommandBase:
    return Sample()
