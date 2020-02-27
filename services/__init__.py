
import typing
from abc import ABCMeta, abstractmethod
from praqta import ApplicationContext

from praqta import CommandBase, ModuleInfo
import importlib
import os
import os.path
import typing
import yaml
import time

# モジュールのキャッシュ
__moduleInfoCache = {}


class ServiceBase(metaclass=ABCMeta):
    @abstractmethod
    def init(self, context: ApplicationContext):
        pass

    @abstractmethod
    def start(self, context: ApplicationContext):
        pass

    @abstractmethod
    def stop(self, context: ApplicationContext):
        pass


def new_instance(service_name: str) -> ServiceBase:
    """
    サービスのインスタンスを返却します

    Parameters
    ----------
    service_name : str
        サービス名

    Returns
    -------
    serviceInstance : ServiceBase
    """
    packageName = f'services.{service_name}.{service_name}'
    need_load = True
    if packageName in __moduleInfoCache:
        # キャッシュからモジュールを取得
        moduleInfo = __moduleInfoCache[packageName]
        need_load = False
        # モジュールのタイムスタンプが新しくなっていたら、モジュール再ロード
        if moduleInfo.is_updated():
            moduleInfo.reload()

    if need_load:
        # モジュールを動的にロード
        moduleInfo = ModuleInfo(service_name,
                                importlib.import_module(packageName))
        # キャッシュに格納
        __moduleInfoCache[packageName] = moduleInfo

    return moduleInfo.new_instance()
