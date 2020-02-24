import typing
import praqta.command_factory as factory
import commands.command_base
from praqta.command_context import CommandContext


def main():
    context = CommandContext()
    commands = []

    for x in range(3):
        command = factory.create_command("sample")
        command.init(context)
        commands.append(command)

    step = 1
    for command in commands:
        context.setStep(step)
        command.proc(context)
        step += 1

    for command in commands:
        command.term(context)
