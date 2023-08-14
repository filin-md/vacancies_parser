import requests

from dbmanager import DBManager


def get_hh_data(list_ids:list, db:DBManager) -> None:
    """Получаем список и объект базы данных и вставляем в базу данных данные поллученные по api"""

    for employer_id in list_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50'
        data = requests.get(url).json()
        insert_data_into_db(data, db)




def insert_data_into_db(data: list[dict], db: DBManager) -> None:
    """Полученные данные из api распаковываем и кладём в базу данных"""
    for item in data['items']:
        employer_id = item['employer']['id']
        employer_name = item['employer']['name']
        title = item['name']
        salary = item['salary']['from'] if item['salary'] else None
        link = item['alternate_url']

        # Здесь должен быть код для вставки данных в таблицы companies и vacancies
        insert_company_query = "INSERT INTO companies (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        insert_vacancy_query = "INSERT INTO vacancies (company_id, title, salary, link) VALUES (%s, %s, %s, %s)"

        db.cursor.execute(insert_company_query, (employer_id, employer_name))
        db.cursor.execute(insert_vacancy_query, (employer_id, title, salary, link))

    db.conn.commit()



# url = f'https://api.hh.ru/vacancies?employer_id=4649269&per_page=50'
# data = get_hh_data(url)
# print(data)