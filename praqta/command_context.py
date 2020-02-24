import typing


class CommandContext(object):
    __step = 0
    __status = 0

    def __init__(self):
        self.__step = 0
        self.__status = 0
        pass

    def setStep(self, step: int):
        self.__step = step

    def getStep(self) -> int:
        return self.__step
