import typing
import praqta.command_factory as factory
from praqta.command_context import CommandContext
from praqta import Row


def main():
    context = CommandContext()
    commands = []

    # スクリプトからコマンド群を順番に生成
    for command_name in ['echo', 'echo']:
        # コマンド名からコマンドインスタンスを作成
        command = factory.new_instance(command_name)

        # コマンド引数の仕様を設定
        context.set_argspec(
            factory.get_command_arg_spec(command_name))

        # コマンド引数を設定
        context.set_args({
            'p1': 'abc',
            'p2': 123,
            'p3': True,
            'targets': ['p1', 'p2', 'p4']
        })

        # コマンドの初期化
        command.init(context)
        # コマンドリストへ追加
        commands.append(command)

    step = 1
    context.set_rows([
        Row({'p1': 'abc', 'p2': 123, 'p3': True}),
        Row({'p1': 'def', 'p2': 456, 'p3': False}),
        Row({'p1': 'ghi', 'p2': 789, 'p3': True}),
    ])
    # コマンド実行処理
    for command in commands:
        context.set_step(step)
        command.proc(context)
        step += 1

    # コマンド修了処理
    for command in commands:
        command.term(context)
