import os
import json
from src.saver import Saver


class JSONWriter(Saver):
    """
    Запись и чтение json
    """
    _file_name = 'vacancies.json'

    @classmethod
    def writer(cls, vacancies: dict):
        """
        Запись в файл
        :return:
        """
        with open(cls._file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)

    @classmethod
    def reader(cls):
        """
        Чтение файла
        :return:
        """
        with open(cls._file_name, 'r', encoding='UTF-8') as file:
            return json.load(file)

