from src.hhapi import HeadHunterAPI
from src.sjapi import SJCred, SuperJobAPI


def hh_interaction(text: str, num_of_vac: str):
    """
    Функция взаимодействия пользователя с парсером HH
    :param text: текст запроса для поиска вакансии
    :param num_of_vac: количество результатов
    :return:
    """
    hh = HeadHunterAPI(text, num_of_vac)

    if num_of_vac == '':
        pass
