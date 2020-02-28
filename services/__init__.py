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
    def init(self, config):
        pass

    @abstractmethod
    def start(self, context):
        pass

    @abstractmethod
    def stop(self, context):
        pass


def get_service(service_name: str) -> ServiceBase:
    if not service_name in __moduleInstanceCache:
        new_instance(service_name)
    return __moduleInstanceCache[service_name]


def stop_service(service_name: str):
    serviceInstances = cast(
        ServiceBase, __moduleInstanceCache[service_name])
    for serviceInstance in serviceInstances:
        serviceInstance.stop()
    __moduleInstanceCache[service_name] = []


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

    if packageName in __moduleInfoCache:
        # キャッシュからモジュールを取得
        moduleInfo = __moduleInfoCache[packageName]
        # モジュールのタイムスタンプが新しくなっていたら、モジュール再ロード
        if moduleInfo.is_updated():
            # サービスのインスタンスをすべて停止
            stop_service(service_name)
            # モジュールのリロード
            moduleInfo.reload()
    else:
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
