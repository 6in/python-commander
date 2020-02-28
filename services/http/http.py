

from .. import ServiceBase
from praqta.interface import ApplicationContext


class HttpService(ServiceBase):
    def init(self, config: dict):
        self.__config = config
        print(f"HttpService.init({config})")

    def start(self, context: ApplicationContext):
        pass

    def stop(self, context: ApplicationContext):
        pass


def new_instance() -> ServiceBase:
    return HttpService()
