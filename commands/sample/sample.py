import typing
from praqta import CommandBase
from praqta.command_context import CommandContext


class Command(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        print("init")
        pass

    def proc(self, context: CommandContext):
        print(f"proc: step={context.get_step()}")
        pass

    def term(self, context: CommandContext):
        print("term")
        pass


def new_instance() -> CommandBase:
    return Command()
