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


class SJAPI(CommonAPI):
    """
    Класс взаимодействия с API superjob.ru
    """

    def __init__(self, api_key):
        self.headers = {'X-Api-App-Id': api_key}
