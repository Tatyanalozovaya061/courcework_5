import psycopg2
import requests


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
        response_vacancies = requests.get(url, params=params).json()
        # if data_vacancies.status_code == 200:
        #     return data_vacancies

        for item in response_vacancies['items']:
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

    params = {
        'area': 1,
        'page': 0,
        'per_page': 50
    }
    employers_data = []
    for employer_id in employer_list:
        url = f"https://api.hh.ru/employers/{employer_id}"
        employer_response = requests.get(url, params).json()

        employer = {
                "employer_id": employer_id,
                "employer_name":  employer_response['name'],
                # "employer_url": ['employer_url']
                }
        employers_data.append(employer)
    return employers_data


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
                employer_name VARCHAR(100) NOT NULL
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


def save_employer_data(employer_data, database_name, params):
    """Сохранение информации о вакансиях и работодателях в базу данных """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employer_data:
            # employer_list = get_employer(employer_list)
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (employer['employer_id'], employer['employer_name'])
            )
    conn.commit()
    conn.close()

def save_vacancies_data(vacancies_data, database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in vacancies_data:
            cur.execute(
                """
                INSERT INTO employers_vacancy (vacancy_id, employer_id, vacancy_name, salary, vacancy_url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (vacancy['vacancy_id'], vacancy['employer_id'], vacancy['vacancies_name'],
                 vacancy['payment'], vacancy['vacancies_url'])
            )

    conn.commit()
    conn.close()
