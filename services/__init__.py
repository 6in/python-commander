
import typing
from abc import ABCMeta, abstractmethod
from praqta import ApplicationContext


class ServiceBase(metaclass=ABCMeta):
    @abstractmethod
    def init(self, context: ApplicationContext):
        pass
