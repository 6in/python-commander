from .. import ServiceBase
from praqta.interface import ApplicationContext


class DatabaseService(ServiceBase):
    def init(self, config: dict):
        self.__dbconfig = config
        print(f"DatabaseService.init({config})")

        # 設定されているDB情報をもとに接続を試してみる
        # 接続できなかったら例外をスローして終了
        for db_name in self.__dbconfig:
            db_conf = self.__dbconfig[db_name]
            print(db_conf['type'])

    def start(self, context: ApplicationContext):
        pass

    def stop(self, context: ApplicationContext):
        pass

    def open(self, dbname: str):
        pass


def new_instance() -> ServiceBase:
    return DatabaseService()
