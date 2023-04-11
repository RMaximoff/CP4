from src.hhapi import HHapi
from src.sjapi import SJapi, SJCred
from utils.utils import hh_interaction


def main():

    request_vacancy = input('Укажите запрос для поиска по вакансиям: ')

    while True:
        choice_platform = input('Выберите с какого сайта необходимо собрать вакансии.\n'
                                '1.HeadHunter\n'
                                '2.SuperJobAPI\n'
                                '3.Со всех\n'
                                'Укажите номер пункта: ')
        if choice_platform == '1':
            num_of_vac = input('Укажите сколько вакансий необходимо подобрать\n'
                               'Если необходимо собрать все существующие вакансии просто нажмите Enter: ')
            hh_interaction(request_vacancy, num_of_vac)
        elif choice_platform == '2':
            break
        elif choice_platform == '3':
            break
        else:
            print("Укажите номер одного из вариантов")







if __name__ == '__main__':
    main()



"""
с какой платформы получаем данные
    хх или сж или обе
поиск по названию вакансии
поиск по зп от - до 
сколько вакансий вывести


"""