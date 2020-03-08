from .. import ServiceBase
from praqta.interface import ApplicationContext, Row, CommandContext, objdict
from praqta.logger import Logger
from typing import cast
import commands as factory
import os.path
import yaml

logger = cast(Logger, None)


def main(script_path: str, config_parameters: dict):
    context = CommandContext()
    commandList = []

    # スクリプトロード
    with open(script_path, 'r') as f:
        script = yaml.load(f, Loader=yaml.FullLoader)
        commands = script['commands']

    # スクリプトパラメータを設定
    script['parameters'].update(config_parameters)
    context.set_script_parameters(script['parameters'])

    logger.info(f"start script '{script_path}'")

    debug_mode = False
    if 'debug' in script['parameters']:
        if type(script['parameters']['debug']) == bool:
            debug_mode = script['parameters']['debug'] == True

    logger.info(f"debug mode = {debug_mode}")

    # スクリプトからコマンド群を順番に生成
    for command in commands:

        command = objdict(command)
        if debug_mode == False and command.debug == True:
            continue

        # コマンド名からコマンドインスタンスを作成
        logger.info(f"create command {command.type}")
        commandInstance = factory.new_instance(command.type, logger)

        # コマンド引数の仕様を設定
        context.set_parameterspec(
            factory.get_command_arg_spec(command.type))

        # コマンド引数を設定
        context.set_parameters(command.parameters)

        # コマンドの初期化
        logger.info(f"init command {command.type}")
        commandInstance.init(context)

        # コマンドリストへ追加
        commandList.append(commandInstance)

    # スクリプトパラメータを１行目のデータとして渡す
    context.set_rows([script['parameters']])

    # コマンド実行処理
    logger.info(f"start command loop")
    while context.is_stop() == False:
        step = 1
        for commandInstance in commandList:
            context.set_step(step)
            # コマンド実行
            commandInstance.proc(context)
            step += 1

    # コマンド終了処理
    logger.info(f"finalize command")
    for commandInstance in commandList:
        commandInstance.term(context)

    return context


class PraqtaService(ServiceBase):
    def init(self, config: dict):
        self.__config = config

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
                context = main(file_path, parameters)
                # 結果を格納
                parameters['context'] = context
                break
            else:
                # スクリプトロード失敗
                logger.error(f'script file not exists. => {file_path}')

    def stop(self, context: ApplicationContext):
        pass


def new_instance(loggerInject: Logger) -> ServiceBase:
    global logger
    logger = loggerInject
    return PraqtaService()
