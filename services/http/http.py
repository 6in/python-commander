

from .. import ServiceBase
from praqta import ApplicationContext


class HttpService(ServiceBase):
    def init(self, context: ApplicationContext):
        self.__config = context.get_config('http')
