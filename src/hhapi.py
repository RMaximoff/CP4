import json

from src.connector import CommonAPI
import requests


class HHapi(CommonAPI):
    """
    Класс взаимодействия с API hh.ru
    """

    def __init__(self, vacancy: str):
        self.headers = {'User-Agent': 'MyApp my-app-feedback@123123.com'}
        self.url_specializations = 'https://api.hh.ru/vacancies'
        self.params = {'text': vacancy}
        self.vacancy_list = self.connect()
        self.out_data_list = []

    def connect(self):
        """
        Метод подключения
        :return:
        """
        r = requests.get(url=self.url_specializations, headers=self.headers, params=self.params).json()['items']
        return [i for i in r]

    def info_vacancy(self):
        """
        Метод приводит вакансии из json в необходимый вид и сохраняет в список out_data_list
        """
        for vacancy in self.vacancy_list:
            vacancy_info = {'name': vacancy['name'],
                            'link': vacancy['alternate_url'],
                            'requirement': vacancy['snippet']['requirement'].replace('<highlighttext>', '')
                            .replace('</highlighttext>', ''),
                            'employer': vacancy['employer']['name'],
                            }
            if vacancy['salary'] is not None:
                if vacancy['salary']['from'] is None:
                    vacancy_info['salary_from'] = 0
                else:
                    vacancy_info['salary_from'] = vacancy['salary']['from']

                if vacancy['salary']['to'] is None:
                    vacancy_info['salary_to'] = 0
                else:
                    vacancy_info['salary_to'] = vacancy['salary']['to']
                vacancy_info['currency'] = vacancy['salary']['currency']
            else:
                vacancy_info['salary_from'] = 0
                vacancy_info['salary_to'] = 0
                vacancy_info['currency'] = ''

            if vacancy.get('responsibility'):
                vacancy_info['responsibility'] = vacancy['responsibility']
            else:
                vacancy_info['responsibility'] = 'Нет описания обязанностей'

            self.out_data_list.append(vacancy_info)

