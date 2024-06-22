# Каталог фильмов

Создание базы данных и демонстрация основных приемов работы 
по обработке данных на примере базы данных каталога фильмов.

В проекте используется: база данных `PosrgreSQL` и библиотека `psycopg2`

Структура проекта.

    movie_catalog
    |-- config.py           конфигурация БД
    |-- core.py             подключение к БД
    |-- main.py             набор демонстрационных примеров
    |-- database        
        |-- creation.py     создание БД и наполнение тестовыми данными
        |-- data.py         коллекции тестовых данных
        |-- requests.py     запросы для выполнения основных операций
        |-- sql_code.py     SQL-код для реализации проекта

Структура базы данных.

* movies - таблица фильмов
* people - таблица персон (актеров, режисеров и т.п.)
* movie_people - связь персон с фильмами
* users - таблица пользователей
* reviews - таблица обзоров фильмов пользователями
* news - таблица новостей

В проекте реализованы следующие основные приемы работы с БД:
* Создание таблиц `CREATE TABLE`
* Создание последовательностей `CREATE SEQUENCE`
* Создание индексов `CREATE INDEX`
* Удаление таблиц `DROP TABLE`
* Создание представлений `CREATE OR REPLACE VIEW`
* Создание хранимых функций `CREATE OR REPLACE FUNCTION`

Для обработки данных реализованы следующие функции:
* `get_movies_all` - получение всех фильмов
* `get_movies_details` - получение всех фильмов c актерами и 
создателями через представление `movie_details_view`
* `get_movies_select` - поиск фильмов по рейтингу и году релиза
* `get_cast_list` - получение списка актеров и создателей в конкретном фильме
* `get_people_movie` - получение списка актеров и создателей в конкретном фильме
через представление `people_movie_view`
* `add_new_movie` - добавление нового фильма в БД
* `update_rating_movie` - обновление рейтинга фильма
* `delete_movie` - удаление фильма из БД
* `add_movie_with_people` - добавление нового фильма вместе 
со списком актеров и создателей через хранимую
процедуру `add_movie_with_people`
* `search_movies_person` - поиск фильмов по неполному имени актеров и авторов
