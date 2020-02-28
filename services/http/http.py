

from .. import ServiceBase
from praqta.interface import ApplicationContext


class HttpService(ServiceBase):
    def init(self, context: ApplicationContext):
        self.__config = context.get_config('http')

    def start(self, context: ApplicationContext):
        pass

    def stop(self, context: ApplicationContext):
        pass


def new_instance() -> ServiceBase:
    return HttpService()
