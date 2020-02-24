import typing
from commands.command_base import CommandBase
from praqta.command_context import CommandContext


class SampleCommand(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        print("init")
        pass

    def proc(self, context: CommandContext):
        print(f"proc: step={context.getStep()}")
        pass

    def term(self, context: CommandContext):
        print("term")
        pass


def new_instance() -> CommandBase:
    return SampleCommand()
