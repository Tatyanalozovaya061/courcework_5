import psycopg2
import requests


# def get_employers_vacancies(all_employers):
#     """Получение данных о работодателях и их вакансиях по API"""
#     # all_employers = [1740, 87021, 2180, 4180, 80, 2343, 78638, 3529, 4023, 543636]
#     employers = []
#     for company in all_employers:
#         url = f'https://api.hh.ru/employers/{company}'
#         employer_response = requests.get(url).json()
#         vacancy_response = requests.get(employer_response['vacancies_url']).json()
#         employers.append({
#             'company': employer_response,
#             'vacancies': vacancy_response['items']
#         })
#     return employers


def get_vacancies(employer_list):
    """Получение данных о вакансиях по API"""

    params = {
        'area': 1,
        'page': 0,
        'per_page': 50
    }
    vacancies_data = []
    for employer_id in employer_list:
        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        data_vacancies = requests.get(url, params=params).json()

        for item in data_vacancies['items']:
            vacancies = {
                'vacancy_id': int(item['id']),
                'vacancies_name': item['name'],
                'payment': item["salary"]["from"] if item["salary"] else None,
                'requirement': item['snippet']['requirement'],
                'vacancies_url': item['alternate_url'],
                'employer_id': employer_id,
            }
            if vacancies['payment'] is not None:
                vacancies_data.append(vacancies)

    return vacancies_data

def get_employer(employer_list):
    """Получение данных о работодателей по API"""

    # params = {
    #     'area': 1,
    #     'page': 0,
    #     'per_page': 50
    # }
    employer_data = []
    for employer_id in employer_list:
        url = f"https://api.hh.ru/employers/{employer_id}"
        data_vacancies = requests.get(url).json()
        for item in data_vacancies:
            employer = {
                "employer_id": employer_id,
                "company_name": ['company_name'],
                #"open_vacancies": ['open_vacancies']
                }
            employer_data.append(employer)
    return employer_data


    # employers = []
    # for employer_id in employer_list:
    #     url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    #     data_vacancies = requests.get(url, params=params).json()
    #     employer_response = requests.get(url).json()
    #     employer_name = employer_response['name']
    #     employer_open_vacancies = employer_response['open_vacancies']
    #     employers.append({'employer': [employer_id, employer_name, employer_open_vacancies]})
    #
    # return employers


def create_database(database_name: str, params: dict):
    """Создание базы данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                employer_name VARCHAR(100) NOT NULL,
                open_vacancies INT
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers_vacancy (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(100) NOT NULL,
                salary INT,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(employer_list):
    """Сохранение информации о вакансиях и работодателях в базу данных """
    conn = psycopg2.connect()

    with conn.cursor() as cur:
        for employer in employer_list:
            employer_list = get_employer()
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, open_vacancies)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (employer_list['employer_id'], employer_list['employer_name'], employer_list['open_vacancies'])
            )

            for vacancy in employer['vacancies']:
                if vacancy['salary'] is None:
                    continue
                else:
                    salary = int(salary)
                vacancy_list = get_vacancies(employer)
                cur.execute(
                    """
                    INSERT INTO employers_vacancy (vacancy_id, employer_id, vacancy_name, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy_list['vacancy_id'], vacancy_list['employer_id'], vacancy_list['vacancy_name'],
                     vacancy_list['salary'], vacancy_list['vacancy_url'])
                )

            conn.commit()
            conn.close()
