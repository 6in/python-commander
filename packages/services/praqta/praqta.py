
import commands as factory
import yaml
from praqta.interface import Row, CommandContext
from .. import ServiceBase
from praqta.interface import ApplicationContext
import os.path


def main(script_path: str):
    context = CommandContext()
    commandList = []

    # スクリプトロード
    with open(script_path, 'r') as f:
        script = yaml.load(f)
        commands = script['commands']

    # スクリプトパラメータを設定
    context.set_script_parameters(script['parameters'])

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
    context.set_rows([script['parameters']])
    while context.is_stop() == False:
        step = 1
        for commandInstance in commandList:
            context.set_step(step)
            # コマンド実行
            commandInstance.proc(context)
            step += 1

    # コマンド終了処理
    for commandInstance in commandList:
        commandInstance.term(context)

    return context


class PraqtaService(ServiceBase):
    def init(self, config: dict):
        self.__config = config
        print(f'PraqtaService.init({config})')

    def start(self, parameters):
        global main

        # スクリプト名を取得
        script = parameters['script_file']
        if script == '':
            return

        # 規定のパスと当てながら、スクリプトが存在したら実行する
        for path in self.__config['scripts']:
            file_path = os.path.join(path, script)
            if os.path.exists(file_path):
                # スクリプト処理実行
                context = main(file_path)
                # 結果を格納
                parameters['context'] = context
                break

    def stop(self, context: ApplicationContext):
        pass


def new_instance() -> ServiceBase:
    return PraqtaService()
