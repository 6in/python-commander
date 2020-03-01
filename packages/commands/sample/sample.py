import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext

rows = [
    Row({'p1': 'abc', 'p2': 123, 'p3': True}),
    Row({'p1': 'def', 'p2': 456, 'p3': False}),
    Row({'p1': 'ghi', 'p2': 789, 'p3': True}),
    Row({'p1': 'abc', 'p2': 123, 'p3': True}),
]


class Sample(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        pass

    def proc(self, context: CommandContext):
        global rows
        print(f"proc: step={context.get_step()}")
        if len(rows) == 0:
            context.set_rows([])
        else:
            row = rows[:2]
            rows = rows[2:]
            context.set_rows(row)

    def term(self, context: CommandContext):
        pass


def new_instance() -> CommandBase:
    return Sample()
