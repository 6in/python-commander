from typing import *


class CommandContext(object):

    def __init__(self):
        self.__step = 0
        self.__status = 0
        self.__rows = []
        pass

    def set_step(self, step: int):
        self.__step = step
        return self

    def get_step(self) -> int:
        return self.__step

    def set_parameters(self, args: dict):
        self.__args = args
        return self

    def get_parameters(self) -> dict:
        return self.__args

    def set_parameterspec(self, spec: dict):
        self.__argspec = spec
        return self

    def get_parameterspec(self) -> dict:
        return self.__argspec

    def set_rows(self, rows: Iterable):
        self.__rows = rows
        return self

    def get_rows(self) -> Iterable:
        return self.__rows

    def get_services(self) -> list:
        return {}

    def get_service(self, service_name: str) -> dict:
        return {}
