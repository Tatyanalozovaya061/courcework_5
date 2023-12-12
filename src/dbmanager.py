import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        # self.database_name = database_name
        # self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, COUNT(vacancy_id) 
            FROM employer 
            JOIN employers_vacancy USING(employer_id)
            GROUP BY employer_name
            """)
            result = cur.fetchall()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, vacancy_name, salary, vacancy_url
            FROM employers_vacancy
            JOIN employers USING(employer_id)
            """)
            result = cur.fetchall()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name ROUND(AVG(salary)) AS average_salary 
            FROM employers
            JOIN vacancy USING (employer_id)
            GROUP BY employer_name
            """)
            result = cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT *
            FROM employers_vacancy
            WHERE salary > (SELECT AVG(salary) FROM employers_vacancy
            """)
            result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with self.conn.cursor() as cur:
            cur.execute(f"""
            SELECT name_vacancy
            FROM employers_vacancy
            WHERE name_vacancy LIKE '%{keyword}%'
            """)
            result = cur.fetchall()
        return result

    def conn_close(self):
        """Закрывает коннект"""
        self.conn.close()
