# coursework_5


- Получает данные о работодателях и их вакансиях с сайта [hh.ru](http://hh.ru/). Для этого используется публичный API [hh.ru](http://hh.ru/) и библиотека `requests`.
- Выбрано 10 интересных мне компаний, от которых получаем данные о вакансиях по API.
- Спроектированы таблицы в БД Postgres для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используется библиотека `psycopg2`.
- Реализован код, который заполняет созданные таблицы в БД Postgres данными о работодателях и их вакансиях.
- Создан класс `DBManager` для работы с данными в БД.