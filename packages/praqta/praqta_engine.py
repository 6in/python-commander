from typing import cast

from services.praqta.praqta import main as praqa_main
import services
from services.database.database import DatabaseService
import yaml


def read_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return yaml.load(f)


def main(config_file: str, script_file: str):

    # プロセス設定ファイルを読み込み
    config = read_config(config_file)
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

    dbService = cast(DatabaseService, services.get_service('database')[0])
    with dbService.open('default') as db:
        dbService.execute_query(db, '''
        insert into products(name,description,price,discount,reg_date)
        values(
            /*name*/'' ,
            /*description*/'' ,
            /*price*/0 ,
            /*discount*/0 ,
            /*reg_date*/''
        )
        ''', {
            'name': 'ssss',
            'description': 'ssaslaksdf',
            'price': 100,
            'discount': 10,
            'reg_date': '2020/02/29 23:59:59',
        })

        c = dbService.execute_query(db, "select * from products", {})
        for row in c:
            print(tuple(row))

    # サービスの停止を行う
    for service_name in service_list:
        services.stop_service(service_name)
