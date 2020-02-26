
from .. import ServiceBase
from praqta import ApplicationContext


class PraqtaService(ServiceBase):
    def init(self, context: ApplicationContext):
        self.__config = context.get_config('praqta')
