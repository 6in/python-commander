from services.database.database import DatabaseService
from services.praqta.praqta import main as praqa_main
from typing import cast
# from praqta.interface import objdict
import services
import yaml

import logging


def read_config(file_path: str) -> dict:
    """
    Configファイル読み込み
    """
    with open(file_path, 'r') as f:
        return yaml.load(f)


def main(config_file: str, script_file: str):

    # プロセス設定ファイルを読み込み
    config = read_config(config_file)

    # ログ設定
    logging.basicConfig(**config["logging"])
    logging.info("start")

    config['parameters']['script_file'] = script_file
    service_list = [x for x in config['services']]

    # サービスの起動を行う
    for service_name in service_list:
        # サービスインスタンスを取得
        service = services.new_instance(service_name)
        # サービスの初期化を行う
        service.init(config[f'{service_name}_service'])
        # サービスの開始
        service.start(config['parameters'])

    # サービスの停止を行う
    for service_name in service_list:
        services.stop_service(service_name)
