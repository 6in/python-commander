import typing
from .. import CommandBase
from praqta.interface import CommandContext, Row


class SampleCommand(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        self.__args = context.get_parameters()
        spec = context.get_parameterspec()
        for x in spec["parameters"]:
            print(x)

    def proc(self, context: CommandContext):
        step = context.get_step()
        targets = self.__args['targets']
        print('================================')
        newRows = []
        for row in context.get_rows():
            newRows.append(row)
            for target in targets:
                value = row[target]
                print(f'echo {step}:{target}={value}')
            print('----------------------------')
        context.set_rows(iter(newRows))

    def term(self, context: CommandContext):
        pass


def new_instance() -> CommandBase:
    return SampleCommand()
