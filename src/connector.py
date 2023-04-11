from abc import ABC, abstractmethod


class CommonAPI(ABC):
    """
    Абстрактный класс для классов HHAPI и SJAPI
    """

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _calculate_num_pages(self):
        pass

    @abstractmethod
    def _get_vacancies(self):
        pass

    @abstractmethod
    def _info_vacancy(self, vacancy_info):
        pass


