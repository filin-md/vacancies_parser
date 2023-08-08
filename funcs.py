import requests

def get_hh_data(url):
    response = requests.get(url)
    return response.json()




def insert_data_into_db(data, db):
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