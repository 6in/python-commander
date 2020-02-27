import typing
#import praqta.command_factory as factory
import commands as factory
# from praqta.command_context import CommandContext
from praqta import Row, CommandContext
import yaml


def main(script_path: str):
    context = CommandContext()
    commandList = []

    # スクリプトロード
    with open(script_path, 'r') as f:
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
        commandList.append(commandInstance)

    # コマンド実行処理
    context.set_rows([{"start": True}])
    while len(context.get_rows()) != 0:
        step = 1
        for commandInstance in commandList:
            context.set_step(step)
            commandInstance.proc(context)
            if len(context.get_rows()) == 0:
                break
            step += 1

    # コマンド終了処理
    for commandInstance in commandList:
        commandInstance.term(context)
