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


def get_vacancies(employer_id):
    """Получение данных о вакансиях по API"""

    params = {
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params=params).json()

    vacancies_data = []
    for item in data_vacancies["items"]:
        vacancies = {
            'vacancy_id': int(item['id']),
            'vacancies_name': item['name'],
            'payment': item["salary"]["from"] if item["salary"] else None,
            'requirement': item['snippet']['requirement'],
            'vacancies_url': item['alternate_url'],
            'employer_id': employer_id
        }
        if vacancies['payment'] is not None:
            vacancies_data.append(vacancies)

        return vacancies_data


def get_employer(employer_id):
    """Получение данных о работодателях по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_company = requests.get(url).json()
    company = {
        "employer_id": int(employer_id),
        "company_name": data_company['name'],
        "open_vacancies": data_company['open_vacancies']
        }

    return company

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
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(100) NOT NULL,
                employer_url TEXT
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


def save_data_to_database(employers, database_name: str, params: dict):
    """Сохранение информации о вакансиях и работодателях в базу данных """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employers:
            company_data = employer['company']
            cur.execute(
                """
                INSERT INTO employers (employer_name, employer_url)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (company_data['name'], f"https://hh.ru/employer/{company_data['id']}")
            )
            employer_id = cur.fetchone()[0]

            for vacancy in employer['vacancies']:
                if vacancy['salary'] is None:
                    continue
                else:
                    salary = int(salary)
                cur.execute(
                    """
                    INSERT INTO employers_vacancy (employer_id, vacancy_name, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancy['name'], salary, f"https://hh.ru/vacancy/{vacancy['id']}")
                )

            conn.commit()
            conn.close()
