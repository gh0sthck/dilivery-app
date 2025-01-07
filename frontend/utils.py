from typing import Any

from app.settings import config

class Context:
    def __init__(self, **kwargs):
        self.__values: dict[Any] = kwargs
        self.__values["title"] = config.name

    @property
    def get_context(self) -> dict[Any]:
        return self.__values


