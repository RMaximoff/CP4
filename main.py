from src.hhapi import HeadHunterAPI
from src.sjapi import SuperJobAPI, SJCred
from src.vacancy import Vacancy
from src.jsonwriter import JSONWriter


def main():
    request_vacancy = input('Укажите запрос для поиска по вакансиям: ')
    choice_platform = input('Выберите с какого сайта необходимо собрать вакансии.\n'
                            '1.HeadHunter\n'
                            '2.SuperJobAPI\n'
                            '3.Со всех\n'
                            'Укажите номер пункта: ')
    num_of_vac = input('Укажите сколько вакансий необходимо подобрать\n'
                       'Если необходимо собрать все существующие вакансии просто нажмите Enter: ')
    while True:
        if choice_platform == '1':
            vacancies = HeadHunterAPI(vacancy=request_vacancy, number_of_vacancy=num_of_vac).found_vacancy
            break
        elif choice_platform == '2':
            vacancies = SuperJobAPI(api_key=SJCred().key,
                                    vacancy=request_vacancy,
                                    number_of_vacancy=num_of_vac).found_vacancy
            break
        elif choice_platform == '3':
            hh = HeadHunterAPI(vacancy=request_vacancy, number_of_vacancy=num_of_vac).found_vacancy
            sj = SuperJobAPI(api_key=SJCred().key, vacancy=request_vacancy, number_of_vacancy=num_of_vac).found_vacancy
            vacancies = hh + sj
            break
        else:
            print("Укажите номер одного из вариантов")
    JSONWriter.writer(vacancies)
    # for i in vacancies:
    #     print(str(Vacancy(i)))
    min_salary = int(input('Укажите минимальную зп для вывода вакансий: '))
    vacancy_list = [Vacancy(i) for i in JSONWriter.reader()]

    for i in vacancy_list:
        if i.min_salary >= min_salary:
            print(i)


if __name__ == '__main__':
    main()
