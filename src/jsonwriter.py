import os
import json


class JSONWriter:
    """
    Запись и чтение json
    """
    def __init__(self):
        self.name_file = 'vacancies.json'

    def write_json(self, vacancies: dict):
        """
        Запись в файл
        :return:
        """
        with open(self.name_file, 'w') as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)

    def read_json(self):
        """
        Чтение файла
        :return:
        """
        with open(self.name_file, 'w') as file:
            json.load(file, indent=4, ensure_ascii=False)

