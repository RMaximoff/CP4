import json

import requests
from src.connector import CommonAPI
import os


class SJCred:
    """
    Класс установки/проверки api ключа для superjob.ru
    """
    def __init__(self):
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


class SJapi(CommonAPI):
    """
    Класс взаимодействия с API superjob.ru
    """
    __URL_SPECIALIZATIONS = 'https://api.superjob.ru/2.0/vacancies/'


    def __init__(self, api_key: str, vacancy: str, number_of_vac: str):
        self.headers = {'X-Api-App-Id': api_key}
        self.url =
        self.params = {'keyword': vacancy,
                       'order_field': 'payment',
                       'order_direction': 'desc'}
        self.vacancy_list = self._connect()

    def _connect(self):
        """
        Метод подключения к api superjob
        :return: список вакансий
        """
        r = requests.get(url=self.url, headers=self.headers, params=self.params)
        return r.json()['objects']

    def _info_vacancy(self, vacancy_info):
        """
        Метод приводит вакансии из json в необходимый вид и сохраняет в список out_data_list
        """
        for vacancy in vacancy_info:
            vacancy_info = {'name': vacancy['profession'],
                            'link': vacancy['link'],
                            'requirement': vacancy['candidat'],
                            'employer': vacancy['client']['title'],
                            'responsibility': vacancy['vacancyRichText'],
                            'salary_from': vacancy['payment_from'],
                            'salary_to': vacancy['payment_to'],
                            'currency': vacancy['currency']}
            vacancy_list.append(vacancy_info)



a = SJapi('v3.r.137482563.90565da25eeae8b8d0612a08e8e717b50f7168b7.68ddd4f56092a57b2e2a0e3f196080624f80f5b1', 'python')
c = a.connect()
print(json.dumps(c, indent=2, ensure_ascii=False))
b = a.info_vacancy()
print(b)