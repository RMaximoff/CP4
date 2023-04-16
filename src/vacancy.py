

class Vacancy:

    def __init__(self, vacancy: dict):

        self._from_website = vacancy['from']
        self._name = vacancy['name']
        self._link = vacancy['link']
        self._employer = vacancy['employer']
        self._salary_from = vacancy['salary_from']
        self._salary_to = vacancy['salary_to']
        self._currency = vacancy['currency']
        self.requirement = vacancy['requirement']

        self._min_salary = self._salary_from if self._salary_from <= self._salary_to else self._salary_to

    def __gt__(self, other):
        """
        Сравнение между вакансиями
        """
        if not isinstance(other, Vacancy):
            raise TypeError('невозможно сравнить')
        if not other._min_salary:
            return True
        if not self._min_salary:
            return False
        return self._min_salary >= other._min_salary

    def __str__(self):
        return f'{self._from_website}\n' \
               f'Заголовок: {self._name}\n' \
               f'Ссылка: {self._link}\n' \
               f'Название компании: {self._employer}\n' \
               f'ЗП от: {self._salary_from} {self._currency}\n' \
               f'ЗП до: {self._salary_to} {self._currency}\n' \
               f'Обязанности: {self.requirement}\n'


