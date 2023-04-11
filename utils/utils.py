from src.hhapi import HHapi
from src.sjapi import SJCred, SJapi


def hh_interaction(text: str, num_of_vac: str):
    """
    Функция взаимодействия пользователя с парсером HH
    :param text: текст запроса для поиска вакансии
    :param num_of_vac: количество результатов
    :return:
    """
    hh = HHapi(text, num_of_vac)

    if num_of_vac == '':
        pass
