import json
from src.connector import CommonAPI


class HeadHunterAPI(CommonAPI):
    """
    Класс взаимодействия с API hh.ru
    На выходе получаем инфу по вакансиям в json формате
    """
    __URL_SPECIALIZATIONS = 'https://api.hh.ru/vacancies'
    __HEADERS = {'User-Agent': 'MyApp my-app-feedback@123123.com'}
    __PER_PAGE = 100  # Кол-во результатов на страницу/1 запрос (из ограничений в api)
    __KEY_FOUND_VACANCY = 'found'  # Ключ к кол-ву результатов по запрашиваемой вакансии
    __KEY_VACANCIES_LIST = 'items'  # Ключ к вакансиям
    __KEY_PARAMS_PAGE = 'page'  # Ключ к параметру номера страницы передаваемой в запросе
    __TIME_SLEEP = 0.26  # вроде бы у HH ограничение на 240 запросов в минуту, поэтому ставлю ожидание

    def __init__(self, vacancy: str, number_of_vacancy: str):
        self.__params = {'text': vacancy,
                         'page': 1,
                         'per_page': self.__PER_PAGE,
                         'order_by': 'salary_desc'}

        super().__init__(url=self.__URL_SPECIALIZATIONS,
                         headers=self.__HEADERS,
                         params=self.__params)
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
        return self._vacancy_dict[self.__KEY_FOUND_VACANCY]

    @property
    def vacancy_list(self):
        """
        Геттер готового списка вакансий
        :return:
        """
        return self._out_vacancy_list

    def _info_vacancy(self, vacancies: list):
        """
        Метод приводит инфо по вакансиям в нужный вид и сохраняет в список.
        :param vacancies: Список вакансий
        """
        for vac in vacancies:
            vacancy_info = {'from': 'HeadHunter',
                            'name': vac.get('name', 'Нет названия'),
                            'link': vac.get('alternate_url', 'Нет ссылки'),
                            'employer': vac['employer'].get('name', 'Название организации не указано'),
                            'salary_from': vac['salary'].get('from', 0),
                            'salary_to': vac['salary'].get('to', 0),
                            'currency': vac['salary'].get('currency', 'Валюта не указана')}

            if vac.get('snippet').get('requirement'):
                vacancy_info['requirement'] = vac['snippet']['requirement'].replace('<highlighttext>', '')\
                                                                           .replace('</highlighttext>', '')
            else:
                vacancy_info['requirement'] = 'Нет описания требований к кандидату'

            self._out_vacancy_list.append(vacancy_info)


a = HeadHunterAPI('водитель категории C', '10')
print(json.dumps(a.vacancy_list,indent=2, ensure_ascii=False))
print(len(a.vacancy_list))