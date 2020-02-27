import typing
#import praqta.command_factory as factory
import commands as factory
from praqta.command_context import CommandContext
from praqta import Row
import yaml


def main(path: str):
    context = CommandContext()
    commandChain = []

    with open(path, 'r') as f:
        script = yaml.load(f)
        commands = script['commands']

    # スクリプトからコマンド群を順番に生成
    for command in commands:
        # コマンド名からコマンドインスタンスを作成
        commandInstance = factory.new_instance(command['type'])

        # コマンド引数の仕様を設定
        context.set_parameterspec(
            factory.get_command_arg_spec(command['type']))

        # コマンド引数を設定
        context.set_parameters(command['parameters'])

        # コマンドの初期化
        commandInstance.init(context)

        # コマンドリストへ追加
        commandChain.append(commandInstance)

    step = 1
    # コマンド実行処理
    for commandInstance in commandChain:
        context.set_step(step)
        commandInstance.proc(context)
        step += 1

    # コマンド修了処理
    for commandInstance in commandChain:
        commandInstance.term(context)
