import typing
from .. import CommandBase
from praqta.interface import CommandContext, Row


class Echo(CommandBase):
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
            row = Row(row)
            newRows.append(row)
            for target in targets:
                value = row[target]
                print(f'echo {step}:{target}={value}')
            print('----------------------------')
        context.set_rows(newRows)

    def term(self, context: CommandContext):
        pass


def new_instance() -> CommandBase:
    return Echo()
