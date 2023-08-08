from config import config
from dbmanager import DBManager
from funcs import get_hh_data, insert_data_into_db


if __name__ == '__main__':

    params = config()
    db = DBManager(dbname='hh_work', **params)
    db.drop_tables()
    db.create_tables()

    employers_ids = [4934, #BeeLine
                    3191643, #Zyfra
                    49357, #Magnit
                    976931, #Skoltech
                    4649269, #Innotech
                    78638, #Tinkoff
                    1995395, #Cybernetic technology
                    4537757, #Antara
                    1740, #Yandex
                    2000762 #IT Space
                     ]

    for employer_id in employers_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50'
        data = get_hh_data(url)
        insert_data_into_db(data, db)

    print(db.get_companies_and_vacansies_count())
    print(db.get_all_vacansies())
    print(db.get_avg_salary())
    print(db.get_vacansies_with_higer_salary())
    print(db.get_vacancies_with_keyword('python'))