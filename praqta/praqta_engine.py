from typing import cast

from services.praqta.praqta import main as praqa_main
import services
import yaml


def read_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return yaml.load(f)


def main(config_file: str, script_file: str):

    # プロセス設定ファイルを読み込み
    config = read_config(config_file)
    config["parameters"]["script_file"] = script_file

    # サービスの起動を行う
    for service_name in config['services']:
        # サービスインスタンスを取得
        service = services.new_instance(service_name)
        # サービスの初期化を行う
        service.init(config[f"{service_name}_service"])
        # サービスの開始
        service.start(config["parameters"])
