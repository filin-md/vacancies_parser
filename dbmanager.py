import psycopg2
class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Здесь должен быть код создания таблиц
        create_companies_table = """
               CREATE TABLE IF NOT EXISTS companies (
                   id SERIAL PRIMARY KEY,
                   name VARCHAR
               )
               """
        create_vacancies_table = """
               CREATE TABLE IF NOT EXISTS vacancies (
                   id SERIAL PRIMARY KEY,
                   company_id INT REFERENCES companies(id),
                   title VARCHAR,
                   salary NUMERIC,
                   link VARCHAR
               )
               """
        self.cursor.execute(create_companies_table)
        self.cursor.execute(create_vacancies_table)
        self.conn.commit()

    def drop_tables(self):
        drop_vacancies_table = "DROP TABLE IF EXISTS vacancies"
        drop_companies_table = "DROP TABLE IF EXISTS companies"
        self.cursor.execute(drop_vacancies_table)
        self.cursor.execute(drop_companies_table)
        self.conn.commit()

    def get_companies_and_vacansies_count(self):
        query = "SELECT companies.name, COUNT(vacancies.id) FROM companies LEFT JOIN vacancies ON companies.id = vacancies.company_id GROUP BY companies.name"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacansies(self):
        query = "SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link FROM vacancies INNER JOIN companies ON vacancies.company_id = companies.id"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacansies_with_higer_salary(self):
        avg_salary = self.get_avg_salary()
        query = "SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link FROM vacancies INNER JOIN companies ON vacancies.company_id = companies.id WHERE vacancies.salary > %s"
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        # Здесь должен быть код для получения вакансий, в названии которых содержится заданное ключевое слово
        query = "SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link FROM vacancies INNER JOIN companies ON vacancies.company_id = companies.id WHERE vacancies.title ILIKE %s"
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()