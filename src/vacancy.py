

class Vacancy:

    def __init__(self,
                 from_website: str,
                 name: str,
                 link: str,
                 employer: str,
                 salary_from,
                 salary_to,
                 currency: str,
                 requirement: str):

        self._from_website = from_website
        self.name = name
        self.link = link
        self.employer = employer
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.requirement = requirement

    def __gt__(self, other):
        """Сравнение между вакансиями"""
        if not isinstance(other, Vacancy):
            raise TypeError('Аргумент должен быть типом Vacancy')
        if not other.salary_from:
            return True
        if not self.salary_from:
            return False
        return self.salary_from >= other.salary_from


