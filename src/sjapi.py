import json

import requests
from src.connector import CommonAPI
import os


class SJCred:
    """
    Класс установки/проверки api ключа для superjob.ru
    """
    def __init__(self, key):
        self.__key_path = os.path.abspath('sj_cred.txt')
        if not self.__check_key():
            self.__write_key(self.__get_key())
        self.key = self.__read_key_file()

    def __check_key(self):
        """
        Проверка наличия файла и ключа в файле
        :return: True если файл существует
        """
        if os.path.exists(self.__key_path) and os.path.getsize(self.__key_path) > 0:
            return True

    def __read_key_file(self):
        """
        Читаем ключ из файла
        """
        with open(self.__key_path, 'r') as file:
            return file.read().strip()

    @staticmethod
    def __get_key():
        """
        Запрашиваем ключ у пользователя
        """
        while True:
            key = input('Укажите Secret key: ')
            if len(key) == 0 or "." not in key:
                print("Кажется вы ничего не указали, либо ключ не соответствует формату. Повторите попытку")
            else:
                break
        return key

    def __write_key(self, key):
        """
        Запись ключа в файл
        """
        with open(self.__key_path, 'w') as file:
            file.write(key)


class SuperJobAPI(CommonAPI):
    """
    Класс взаимодействия с API superjob.ru
    """
    __URL_SPECIALIZATIONS = 'https://api.superjob.ru/2.0/vacancies/'
    __PER_PAGE = 100  # Кол-во результатов на страницу/1 запрос (из ограничений в api)
    __KEY_FOUND_VACANCY = 'total'  # Ключ к кол-ву результатов по запрашиваемой вакансии
    __KEY_VACANCIES_LIST = 'objects'  # Ключ к вакансиям
    __KEY_PARAMS_PAGE = 'page'  # Ключ к параметру номера страницы передаваемой в запросе
    __TIME_SLEEP = 0.55  # ограничение в 120 запросов в минуту

    def __init__(self, api_key: str, vacancy: str, number_of_vacancy: str):
        self.__headers = {'X-Api-App-Id': api_key}
        self.__params = {'page': 1,
                         'count': self.__PER_PAGE,
                         'keyword': vacancy,
                         'order_field': 'payment',
                         'order_direction': 'desc'}

        super().__init__(url=self.__URL_SPECIALIZATIONS, headers=self.__headers, params=self.__params)
        self._connect()
        self._calculate_num_pages(number_of_vac=number_of_vacancy,
                                  key_found_vacancy=self.__KEY_FOUND_VACANCY,
                                  per_page=self.__PER_PAGE)
        self._get_vacancies(key_vacancies_list=self.__KEY_VACANCIES_LIST,
                            key_page=self.__KEY_PARAMS_PAGE,
                            time_sleep=self.__TIME_SLEEP)

    @property
    def found_vacancy(self):
        """
        Геттер кол-ва вакансий
        :return: int кол-во вакансий
        """
        return self._out_vacancy_list

    def _info_vacancy(self, vacancies):
        """
        Метод приводит вакансии из json в необходимый вид и сохраняет в список out_data_list
        """

        for vac in vacancies:
            vacancy_info = {'from': 'SuperJob',
                            'name': vac.get('profession', "Вакансия без названия"),
                            'link': vac.get('link', 'Нет ссылки'),
                            'employer': vac['client']['title'],
                            'requirement': vac.get('candidat', 'Нет описания требований к кандидату'),
                            'salary_from': vac.get('payment_from', 0),
                            'salary_to': vac.get('salary_to', 0),
                            'currency': vac.get('currency', 'Валюта не указана')}

            if vac.get('client'):
                if vac['client'].get('title'):
                    vacancy_info['employer'] = vac['client']['title']
            else:
                vacancy_info['employer'] = 'Название организации не указано'

            self._out_vacancy_list.append(vacancy_info)

a = SuperJobAPI('v3.r.137490855.2c549747f51cb5ae390c435ba5f403be0973ea19.39fa72f7a03a5e9e8ed5b8ec18df24eb7e431afb', 'python', '10')
print(json.dumps(a.found_vacancy, indent=2, ensure_ascii=False))
print(len(a.found_vacancy))

