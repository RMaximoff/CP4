from abc import ABC, abstractmethod
import requests
import math
import time


class CommonAPI(ABC):
    """
    Общий класс для классов HeadHunterAPI и SuperJobAPI
    """
    def __init__(self, url: str, headers: dict, params: dict):
        self._out_vacancy_list = []
        self._url = url
        self._headers = headers
        self._params = params
        self._pages = 1
        self._vacancy_dict = {}

    def _connect(self):
        """
        Метод создает запрос к api сайта
        """

        r = requests.get(url=self._url, headers=self._headers, params=self._params)
        if r.status_code == 200:
            self._vacancy_dict.update(r.json())
        else:
            print(f'Произошла ошибка при подключении к источникам данных.\n'
                  f'Код ошибки{r.status_code}')
            exit()

    def _get_vacancies(self, key_vacancies_list: str, key_page: str, time_sleep: float):
        """
        Получаем необходимое кол-во вакансий
        :param key_vacancies_list: Ключ к вакансиям
        :param key_page: Ключ к параметру номера страницы передаваемой в запросе
        :param time_sleep: время между циклами
        """
        for i in range(1, self._pages + 1):
            self._params[key_page] = i
            self._connect()
            self._info_vacancy(self._vacancy_dict[key_vacancies_list])
            time.sleep(time_sleep)

    def _calculate_num_pages(self, number_of_vac: str, key_found_vacancy: str, per_page: int):
        """
        Рассчитываем сколько запросов необходимо сделать, чтобы получить необходимое кол-во вакансий.
        :param number_of_vac: Сколько вакансий нужно получить
        :param key_found_vacancy: Ключ к кол-ву результатов по запрашиваемой вакансии
        :param per_page: Кол-во результатов на страницу
        """
        if number_of_vac == '':
            self._pages = math.ceil(self._vacancy_dict[key_found_vacancy] / per_page)
        else:
            self._pages = math.ceil(int(number_of_vac) / per_page)

    @abstractmethod
    def _info_vacancy(self, vacancy_info):
        pass


