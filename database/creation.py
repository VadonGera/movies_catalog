from core import connect_database as connection
from database.sql_code import (
    sql_deletion_tables,
    sql_create_table_movies, sql_create_table_people, sql_create_table_movie_people,
    sql_create_table_users, sql_create_table_reviews, sql_create_table_news,
    sql_create_view_people_movie, sql_create_view_movie_details,
    sql_create_function_add_movie_with_people
)
from database.data import (
    data_movies, data_movies_people, data_people,
    data_user, data_reviews, data_news
)


def create_database():
    conn = None
    try:
        conn = connection()
        cursor = conn.cursor()

        # Удаляем таблицы
        cursor.execute(sql_deletion_tables)

        # Создаем таблицы
        cursor.execute(sql_create_table_movies)
        cursor.execute(sql_create_table_people)
        cursor.execute(sql_create_table_movie_people)
        cursor.execute(sql_create_table_users)
        cursor.execute(sql_create_table_reviews)
        cursor.execute(sql_create_table_news)
        # conn.commit()

        # Создаем представление для вывода актеров и фильмов с их участием
        cursor.execute(sql_create_view_people_movie)

        # Создаем представление для вывода всех фильмов cо всеми актерами и создателями
        cursor.execute(sql_create_view_movie_details)

        # Создаем процедуру для добавления нового фильма вместе с актерами
        cursor.execute(sql_create_function_add_movie_with_people)

        # Заполеяем таблицы тестовыми данными
        query_insert = "INSERT INTO movies VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.executemany(query_insert, data_movies)

        query_insert = "INSERT INTO people VALUES (%s, %s, %s);"
        cursor.executemany(query_insert, data_people)

        query_insert = "INSERT INTO movie_people VALUES (%s, %s, %s);"
        cursor.executemany(query_insert, data_movies_people)

        query_insert = "INSERT INTO users VALUES (%s, %s, %s, %s);"
        cursor.executemany(query_insert, data_user)

        query_insert = "INSERT INTO reviews VALUES (%s, %s, %s, %s, %s);"
        cursor.executemany(query_insert, data_reviews)

        query_insert = "INSERT INTO news VALUES (%s, %s, %s, %s, %s);"
        cursor.executemany(query_insert, data_news)

        conn.commit()

    except conn.Error as e:
        if conn:
            conn.rollback()
            print("Ошибка создания базы данных", e)
    finally:
        if conn:
            conn.close()
