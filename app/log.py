import logging

from .settings import config


class AppLogger:
    def __init__(self, name: str):
        self.name = name
        self.__logger = logging.getLogger(self.name)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt=config.logs.fmt, datefmt=config.logs.datefmt, style=config.logs.style
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def get_logger(self):
        return self.__logger

    def set_level(self, level):
        self.__logger.setLevel(level)
        return self.__logger
