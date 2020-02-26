

from .. import ServiceBase
from praqta import ApplicationContext


class DatabaseService(ServiceBase):
    def init(self, context: ApplicationContext):
        self.__dbconfig = context.get_config('databases')

        for config in self.__dbconfig:
            type = config['type']
            print(type)
