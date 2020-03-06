from services.database.database import DatabaseService
from services.praqta.praqta import main as praqa_main
from typing import cast
# from praqta.interface import objdict
import services
import yaml
from praqta.logger import Logger
import praqta.logger


def read_config(file_path: str) -> dict:
    """
    Configファイル読み込み
    """
    with open(file_path, 'r') as f:
        return yaml.load(f)


def main(config_file: str, script_file: str, extra_args: list):

    # プロセス設定ファイルを読み込み
    config = read_config(config_file)

    # ログ設定
    Logger.set_properties(config["logging"])
    loggerParent = Logger()
    logger = loggerParent.logger

    logger.info("start")

    # スクリプトファイル名を保存
    config['parameters']['script_file'] = script_file

    # 拡張引数をパラメータに格納
    for extra_arg in extra_args:
        tokens = extra_arg.split("=")
        if len(tokens) == 2:
            if tokens[1].lower() == "true":
                tokens[1] = True
            elif tokens[1].lower() == "false":
                tokens[1] = False
            config['parameters'][tokens[0]] = tokens[1]
        elif len(tokens) == 1:
            if tokens[0][0] == "!":
                # 変数の先頭に！が付いていたらFalseを設定
                config['parameters'][tokens[0][1:]] = False
            else:
                # 変数にTrueを設定
                config['parameters'][tokens[0]] = True

    service_list = [x for x in config['services']]

    # サービスの起動を行う
    for service_name in service_list:
        # サービスインスタンスを取得
        service = services.new_instance(service_name, logger)
        logger.info(f"create service = {service_name}")
        # サービスの初期化を行う
        service.init(config[f'{service_name}_service'])
        # サービスの開始
        service.start(config['parameters'])

    # サービスの停止を行う
    for service_name in service_list:
        services.stop_service(service_name)
