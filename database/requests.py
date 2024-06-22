from core import connect_database as connection


# Список всех фильмов
def get_movies_all():
    conn = connection()
    with conn.cursor() as cursor:
        query_select = "SELECT * FROM movies ORDER BY movie_title ASC;"
        cursor.execute(query_select)
        conn.commit()
        return cursor.fetchall()

# Список всех фильмов cо всеми персонами через представление 'sql_create_view_movie_details'
def get_movies_details():
    conn = connection()
    with conn.cursor() as cursor:
        query_select = "SELECT * FROM movie_details_view;"
        cursor.execute(query_select)
        conn.commit()
        return cursor.fetchall()

# Поиск фильмов по рейтингу и дате выпуска
def get_movies_select(rating: float = 1, year: int = 1980):
    conn = connection()
    with conn.cursor() as cursor:
        query_select = """
            SELECT * 
                FROM movies 
                WHERE movie_rating >= %s AND EXTRACT(YEAR FROM movie_release) >= %s
                ORDER BY movie_title;
        """
        cursor.execute(query_select % (rating, year))
        conn.commit()
        return cursor.fetchall()


# Список актеров и их ролей в конкретном фильме id
def get_cast_list(movie_id: int):
    conn = connection()
    with conn.cursor() as cursor:
        query_select = """
            SELECT people.people_name, people.people_role 
                FROM people
                JOIN movie_people ON people.people_id = movie_people.mp_people_id
                WHERE movie_people.mp_movie_id = %s;
        """
        cursor.execute(query_select % movie_id)
        conn.commit()
        return cursor.fetchall()


# Поиск фильмов по персонам
def search_movies_person(search_str: str):
    conn = connection()
    with conn.cursor() as cursor:
        query_select = """
            SELECT m.*
                FROM people p
                JOIN movie_people ON p.people_id = movie_people.mp_people_id
                JOIN movies m ON movie_people.mp_movie_id = m.movie_id
                WHERE lower(p.people_name) LIKE lower('%%%s%%')
                ORDER BY m.movie_title;
        """

        cursor.execute(query_select % search_str)
        conn.commit()
        return cursor.fetchall()

# Добавление нового фильма
def add_new_movie(new_movie: tuple):
    conn = connection()
    with conn.cursor() as cursor:
        query_insert = """
            INSERT INTO movies (movie_title, movie_release, movie_genre, movie_rating, movie_description) 
                VALUES (%s, %s, %s, %s, %s) RETURNING movie_id;
        """
        cursor.execute(query_insert, new_movie)
        conn.commit()
        return cursor.fetchone()[0]


# Удаление фильма по id
def delete_movie(movie_id: int):
    conn = connection()
    with conn.cursor() as cursor:
        query_delete = """
            DELETE FROM movies WHERE movie_id = %s
                RETURNING movie_id;
        """
        cursor.execute(query_delete % movie_id)
        conn.commit()
        return cursor.fetchone()[0]


# Обновляем рейтинг фильма
def update_rating_movie(movie_id: int, rating: float):
    conn = connection()
    with conn.cursor() as cursor:
        query_update = """
            UPDATE movies 
                SET movie_rating = %s 
                WHERE movie_id = %s 
                RETURNING movie_title, movie_rating;
        """
        cursor.execute(query_update % (rating, movie_id))
        conn.commit()
        return cursor.fetchone()


# Добавление нового фильма вместе со списком актеров через хранимую функцию 'add_movie_with_people'
def add_movie_with_people(movie: tuple, people: tuple):
    conn = connection()
    with conn.cursor() as cursor:
        cursor.callproc('add_movie_with_people', (movie[0], movie[1], movie[2], movie[3], movie[4], list(people)))
        conn.commit()
        return cursor.fetchone()[0]


# Список актеров в конкретном фильме через представление 'people_movie_view'
def get_people_movie(movie_id: int):
    conn = connection()
    with conn.cursor() as cursor:
        query_select = """
            SELECT people_name, people_role, movie_title FROM people_movie_view WHERE movie_id = %s;
        """
        cursor.execute(query_select % movie_id)
        conn.commit()
        return cursor.fetchall()
