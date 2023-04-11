import json
from src.connector import CommonAPI
import math
import requests
import time


class HHapi(CommonAPI):
    """
    Класс взаимодействия с API hh.ru
    На выходе получаем инфу по вакансиям в json формате
    """
    __URL_SPECIALIZATIONS = 'https://pi.hh.ru/vacancies'
    __HEADERS = {'User-Agent': 'MyApp my-app-feedback@123123.com'}
    __PER_PAGE = 100

    def __init__(self, vacancy: str, number_of_vac: str):
        self.__number_of_vac = number_of_vac
        self.__params = {'text': vacancy,
                         'page': 1,
                         'per_page': self.__PER_PAGE,
                         'order_by': 'salary_desc'}
        self.__vacancy_dict = {}
        self.__pages = 0
        self.__out_vacancy_list = []

        self._connect()
        self._calculate_num_pages()
        self._get_vacancies()

    @property
    def found_vacancy(self):
        """
        Геттер кол-ва вакансий
        :return: int кол-во вакансий
        """
        return self.__vacancy_dict['found']

    @property
    def vacancy_list(self):
        """
        Геттер готового списка вакансий
        :return:
        """
        return self.__out_vacancy_list

    def _connect(self):
        """
        Подключаемся к api hh.ru
        """
        try:
            r = requests.get(url=self.__URL_SPECIALIZATIONS, headers=self.__HEADERS, params=self.__params)
            if r.status_code == 200:
                self.__vacancy_dict.update(r.json())
        except requests.exceptions.RequestException as e:
            print(f'Произошла ошибка при подключении к HH.ru: {e}')

    def _calculate_num_pages(self):
        """
        Рассчитываем сколько запросов необходимо сделать, чтобы получить необходимое кол-во вакансий
        :return: кол-во запросов
        """
        if self.__number_of_vac == '':
            self.__pages = math.ceil(self.__vacancy_dict['found'] / self.__PER_PAGE)
        else:
            self.__pages = math.ceil(int(self.__number_of_vac) / self.__PER_PAGE)

    def _get_vacancies(self):
        """
        Получаем нужное кол-во вакансий
        """
        for i in range(1, self.__pages+1):
            self.__params['page'] = i
            self._connect()
            self._info_vacancy(self.__vacancy_dict['items'])
            time.sleep(0.26)  # вроде бы у HH ограничение на 240 запросов в минуту, поэтому ставлю ожидание

    def _info_vacancy(self, vacancies: list):
        """
        Метод приводит инфо по вакансиям в нужный вид и сохраняет в список.
        :param vacancies: Список вакансий
        """

        for vac in vacancies:
            vacancy_info = {'name': vac['name'],
                            'link': vac['alternate_url'],
                            'employer': vac['employer']['name']}

            if vac['snippet']['requirement'] is not None:
                vacancy_info['requirement'] = vac['snippet']['requirement'].replace('<highlighttext>', '')\
                                                                            .replace('</highlighttext>', '')
            else:
                vacancy_info['requirement'] = 'Нет описания требований к кандидату'

            if vac['salary'] is not None:
                if vac['salary']['from'] is None:
                    vacancy_info['salary_from'] = 0
                else:
                    vacancy_info['salary_from'] = vac['salary']['from']

                if vac['salary']['to'] is None:
                    vacancy_info['salary_to'] = 0
                else:
                    vacancy_info['salary_to'] = vac['salary']['to']
                vacancy_info['currency'] = vac['salary']['currency']
            else:
                vacancy_info['salary_from'] = 0
                vacancy_info['salary_to'] = 0
                vacancy_info['currency'] = ''

            if vac.get('responsibility'):
                vacancy_info['responsibility'] = vac['responsibility']
            else:
                vacancy_info['responsibility'] = 'Нет описания обязанностей'
            self.__out_vacancy_list.append(vacancy_info)


a = HHapi('водитель категории C', '600')
print(json.dumps(a.vacancy_list, indent=2, ensure_ascii=False))
print(len(a.vacancy_list))

