from abc import ABC, abstractmethod


class Saver(ABC):
    """
    Запись полученных вакансий в файл json
    """
    @abstractmethod
    def writer(self, vacancies: dict):
        pass

    @abstractmethod
    def reader(self):
        pass

