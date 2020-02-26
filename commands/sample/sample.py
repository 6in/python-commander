import typing
from praqta import CommandBase, Row
from praqta.command_context import CommandContext


class Sample(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        pass

    def proc(self, context: CommandContext):
        print(f"proc: step={context.get_step()}")
        context.set_rows([
            Row({'p1': 'abc', 'p2': 123, 'p3': True}),
            Row({'p1': 'def', 'p2': 456, 'p3': False}),
            Row({'p1': 'ghi', 'p2': 789, 'p3': True}),
        ])

    def term(self, context: CommandContext):
        pass


def new_instance() -> CommandBase:
    return Sample()
