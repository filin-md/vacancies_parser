from decimal import Decimal

import psycopg2
class DBManager:
    def __init__(self, dbname:str, user:str, password:str, host:str, port:str) -> None:
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()

    def create_tables(self) -> None:
        """Создаём две таблицы - companies и vacancies"""
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
                   title VARCHAR(255),
                   salary NUMERIC,
                   link VARCHAR(255)
               )
               """
        self.cursor.execute(create_companies_table)
        self.cursor.execute(create_vacancies_table)
        self.conn.commit()

    def drop_tables(self) -> None:
        """Удаляем таблицы если они существуют"""
        drop_vacancies_table = "DROP TABLE IF EXISTS vacancies"
        drop_companies_table = "DROP TABLE IF EXISTS companies"
        self.cursor.execute(drop_vacancies_table)
        self.cursor.execute(drop_companies_table)
        self.conn.commit()

    def get_companies_and_vacansies_count(self) -> list[tuple]:
        """Получаем количество вакансий в каждой из компаний"""
        query = ("SELECT companies.name, COUNT(vacancies.id) "
                 "FROM companies "
                 "LEFT JOIN vacancies ON companies.id = vacancies.company_id "
                 "GROUP BY companies.name")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacansies(self) -> list[tuple]:
        """Выводим название компании, название вакансии, зарплату и ссылку всех существующих вакансий"""
        query = ("SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link "
                 "FROM vacancies "
                 "INNER JOIN companies ON vacancies.company_id = companies.id")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Decimal:
        """Получаем среднюю зарплату по всем вакангсиям"""
        query = ("SELECT AVG(salary) "
                 "FROM vacancies "
                 "WHERE salary IS NOT NULL")
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacansies_with_higer_salary(self) -> list[tuple]:
        """Выводим вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        query = ("SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link "
                 "FROM vacancies "
                 "INNER JOIN companies ON vacancies.company_id = companies.id "
                 "WHERE vacancies.salary > %s")
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Выводим все вакансии в названии которых содержится ключевое слово"""
        query = ("SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link "
                 "FROM vacancies "
                 "INNER JOIN companies ON vacancies.company_id = companies.id "
                 "WHERE vacancies.title ILIKE %s")
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()