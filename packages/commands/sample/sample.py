import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext
from typing import cast
from logging import Logger

import json
import yaml

logger = cast(Logger, {})


class Sample(CommandBase):
    def __init__(self):
        pass

    def init(self, context: CommandContext):
        # パラメータを取得する
        self.__params = context.get_parameters()
        self.__rows = []
        context.set_supplier(self)
        self.__has_data = True

        try:
            dataType = self.__params.data_type
            if dataType == 'csv':
                lines = self.__params.data.split('\n')
                head = [x.rstrip() for x in lines[0].split(',')]
                data = [line for line in lines[1:] if not line.strip() == ""]
                for row in data:
                    row = [x.rstrip() for x in row.split(',')]
                    newData = {}
                    for i in range(len(head)):
                        newData[head[i]] = row[i]
                    self.__rows.append(newData)
            if dataType == 'json':
                self.__rows = json.loads(self.__params.data)
            if dataType == 'yaml':
                self.__rows = yaml.load(self.__params.data)
            if dataType == 'object':
                if type(self.__params.data) == list:
                    self.__rows = self.__params.data
                else:
                    logger.error('データ型がlist構造になっていません')
        except Exception as e:
            logger.error(e)
            raise e

    def proc(self, context: CommandContext):
        rows = self.__rows
        context.set_rows(rows)
        self.__has_data = False

    def term(self, context: CommandContext):
        pass

    def has_data(self):
        return self.__has_data


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject
    return Sample()
