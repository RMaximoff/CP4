import json

from src.connector import CommonAPI
import requests


class HHapi(CommonAPI):
    """
    Класс взаимодействия с API hh.ru
    """

    def __init__(self, vacancy: str):
        self.headers = {'User-Agent': 'MyApp my-app-feedback@123123.com'}
        self.vacancy = vacancy
        self.url_specializations = 'https://api.hh.ru/vacancies'
        self.vacancy_list = self.connect()
        self.out_data_list = self.info_vacancy()

    def connect(self):
        """
        Подключаемся к api hh.ru
        :return:
        """
        params = {'text': self.vacancy,
                       }
        r = requests.get(url=self.url_specializations, headers=self.headers, params=self.params)
        if r.status_code == 200:
            return [i for i in r.json()['items']]
        else:
            print(f'При подключении к HH.ru произошла ошибка. Код ошибки {r.status_code}')
            exit()

    def info_vacancy(self):
        """
        Метод приводит вакансии из json в необходимый вид и сохраняет в список out_data_list
        """
        vacancy_list = []
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
            vacancy_list.append(vacancy_info)

        return vacancy_list


a = HHapi('python')
print(a.out_data_list)