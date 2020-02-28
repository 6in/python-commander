from abc import ABCMeta, abstractmethod
from praqta.interface import ModuleInfo
import importlib
import os
import os.path
import time
from typing import cast
import yaml

# モジュールのキャッシュ
__moduleInfoCache = {}

# モジュールのインスタンスのキャッシュ
__moduleInstanceCache = {}


class ServiceBase(metaclass=ABCMeta):
    @abstractmethod
    def init(self, context):
        pass

    @abstractmethod
    def start(self, context):
        pass

    @abstractmethod
    def stop(self, context):
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
            # サービスのインスタンスをすべて停止
            serviceInstances = cast(
                ServiceBase, __moduleInstanceCache[service_name])
            for serviceInstance in serviceInstances:
                serviceInstance.stop()
            __moduleInstanceCache[service_name] = []
            moduleInfo.reload()

    if need_load:
        # モジュールを動的にロード
        moduleInfo = ModuleInfo(service_name,
                                importlib.import_module(packageName))
        # キャッシュに格納
        __moduleInfoCache[packageName] = moduleInfo

    # インスタンスを生成
    serviceInstance = moduleInfo.new_instance()

    # サービスインスタンスのキャッシュへ格納
    if not service_name in __moduleInstanceCache:
        __moduleInstanceCache[service_name] = []
    __moduleInstanceCache[service_name].append(serviceInstance)

    return serviceInstance
