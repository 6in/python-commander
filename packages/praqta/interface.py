
from typing import Iterable
from abc import ABCMeta, abstractmethod
import importlib
import os
import os.path
import time
import typing
import yaml
import re

rePlaceHolder = re.compile(r"(\$\{(\w+)\})")


class objdict(dict):

    def __init__(self, src):
        super().__init__(src)

    def set_source(self, props: dict):
        self.__props = objdict(props)
        return self

    def embed_place_holder(self, value):
        if type(value) == str:
            for (tgt, key) in rePlaceHolder.findall(value):
                rep = self.__props[key]
                value = value.replace(tgt, rep)
        elif type(value) == list:
            return [self.embed_place_holder(x) for x in value]

        return value

    def get(self, name):
        if name in self:
            return self.embed_place_holder(self[name])
        elif name in self.__props:
            return self.embed_place_holder(self.__props[name])
        else:
            raise AttributeError("No such attribute: " + name)

    def get_system_parameter(self, name: str):
        return self.__props[name]

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class ApplicationContext(object):
    def __init__(self):
        pass

    def read_config(self, path: str):
        with open(path, 'r') as f:
            self.__config = yaml.load(f)
        return self

    def get_config(self, section: str) -> dict:
        return self.__config[section]


class CommandContext(object):

    def __init__(self):
        self.__step = 0
        self.__status = 0
        self.__stop = False
        self.__rows = []
        self.__supplieres = []
        self.__script_parameters = {}

    def set_step(self, step: int):
        self.__step = step
        return self

    def get_step(self) -> int:
        return self.__step

    def set_parameters(self, args: dict):
        self.__args = args
        return self

    def get_parameters(self) -> dict:
        return objdict(self.__args).set_source(self.get_script_parameters())

    def set_parameterspec(self, spec: dict):
        self.__argspec = spec
        return self

    def get_parameterspec(self) -> dict:
        return self.__argspec

    def set_script_parameters(self, props: dict):
        self.__script_parameters = props
        return self

    def get_script_parameters(self, ) -> dict:
        return self.__script_parameters

    def set_rows(self, rows: Iterable):
        self.__rows = rows
        return self

    def get_rows(self) -> Iterable:
        return self.__rows

    def get_services(self) -> list:
        return {}

    def get_service(self, service_name: str) -> dict:
        return {}

    def set_stop(self):
        self.__stop = True

    def is_stop(self):
        count = len(self.__supplieres)
        return count == len([x for x in self.__supplieres if x.has_data() == False])

    def set_supplier(self, obj: object):
        self.__supplieres.append(obj)
        return self


class ModuleInfo(object):

    def __init__(self, name, module):
        self.__module = module
        self.__file = module.__file__
        self.__timestamp = os.stat(self.__file).st_mtime
        self.load_spec()

    def load_spec(self):
        # Yamlファイルをロード
        (path, _) = os.path.splitext(self.__file)
        with open(f'{path}.yml', 'r') as f:
            self.__spec = yaml.load(f, Loader=yaml.FullLoader)
            # todo: json schemaによるspecのチェック

    def get_spec(self) -> dict:
        return self.__spec

    def is_updated(self):
        return os.stat(self.__file).st_mtime > self.__timestamp

    def get_module(self):
        return self.__module

    def reload(self):
        importlib.reload(self.__module)
        return self

    def new_instance(self, logger):
        return self.__module.new_instance(logger)


class Row(object):
    def __init__(self, row: dict):
        if type(row) == Row:
            self.__row = row.__row
        else:
            self.__row = row

    def get(self, name: str):
        if self.__row == None:
            return None
        keys = self.__row.keys()
        if name in keys:
            return self.__row[name]
        elif name.upper() in keys:
            return self.__row[name.upper()]
        elif name.lower() in keys:
            return self.__row[name.lower()]
        else:
            return None

    def set(self, key: str, value):
        self.__row[key] = value

    def __getitem__(self, name: str):
        self.get(name)

    def raw(self) -> dict:
        return self.__row

    def keys(self):
        if self.__row == None:
            return []
        return self.__row.keys()
