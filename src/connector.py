from abc import ABC, abstractmethod
import requests


class CommonAPI(ABC):
    """
    Абстрактный класс для классов HHAPI и SJAPI
    """

    @abstractmethod
    def connect(self, url: str, headers: dict):
        return requests.get(url=url, headers=headers)

