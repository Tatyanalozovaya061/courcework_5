from src.utils import get_vacancies, get_employer, create_database, save_vacancies_data, save_employer_data
from src.config import config
from pprint import pprint
from src.dbmanager import DBManager


def main():
    """
    Основная функция программы
    """
    print("Привет! Это программа поможет найти вакансии на hh.ru и объединить их в единую базу данных\n"
          "Введите желаемое название базы данных, в которой будет храниться информация: ")
    database_name = input()
    params = config()

    employer_list = [3959909, 1740, 87021, 2180, 80, 2343, 78638, 3529, 4023, 543636]

    while True:
        command = input("1. Получить список всех компаний и количество вакансий у каждой компании;\n"
                            "2. Получить список всех вакансий с указанием названия компании, названия вакансии и "
                            "зарплаты и ссылки на вакансию;\n"
                            "3. Получить среднюю зарплату по вакансиям;\n"
                            "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n"
                            "5. Получить список всех вакансий по ключевому слову;\n"
                            "0. Завершить программу.\n"
                            "Введите команду: ")


        create_database(database_name, params)
        save_employer_data(get_employer(employer_list), database_name, params)
        save_vacancies_data(get_vacancies(employer_list), database_name, params)
        dbmanager = DBManager(database_name, params)
        print("База данных создана")

        if command == "0":
            print('Завершение работы.')
            break
        elif command == '1':
            print(dbmanager.get_companies_and_vacancies_count())
            print()
        elif command == '2':
            print(dbmanager.get_all_vacancies())
            print()
        elif command == '3':
            print(dbmanager.get_avg_salary())
            print()
        elif command == '4':
            print(dbmanager.get_vacancies_with_higher_salary())
            print()
        elif command == '5':
            keyword = input('Введите ключевое слово: ')
            answer = dbmanager.get_vacancies_with_keyword(keyword)
            if answer:
                print(answer)
            else:
                print('Ничего не найдено.')
            print()
        else:
            print('Некорректный ввод. Повторите попытку.')


if __name__ == '__main__':
    main()
