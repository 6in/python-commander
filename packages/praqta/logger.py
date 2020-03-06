from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG

logger = None


def set_logger(l):
    global logger
    logger = l


class Logger:
    props = {
        'filename': './logs/server.log',
        'level': DEBUG
    }

    @staticmethod
    def set_properties(props: dict):
        Logger.props = props

    def __init__(self, name='paqta'):
        self.logger = getLogger(name)
        self.logger.propagate = True
        level = Logger.props["level"]
        self.logger.setLevel(level)
        formatter = Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s] [%(funcName)s] %(message)s")

        # stdout
        handler = StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        # file
        handler = handlers.RotatingFileHandler(filename=Logger.props["filename"],
                                               maxBytes=1048576,
                                               backupCount=3)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
