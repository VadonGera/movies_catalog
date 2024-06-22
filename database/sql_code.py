sql_deletion_tables = """
    DROP TABLE IF EXISTS movies CASCADE;
    DROP TABLE IF EXISTS movie_people;
    DROP TABLE IF EXISTS people;
    DROP TABLE IF EXISTS reviews;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS news;
    DROP SEQUENCE IF EXISTS movie_id_seq;
    DROP SEQUENCE IF EXISTS people_id_seq;
    DROP SEQUENCE IF EXISTS mp_id_seq;
    DROP SEQUENCE IF EXISTS user_id_seq;
    DROP SEQUENCE IF EXISTS review_id_seq;
"""

sql_create_table_movies = """
    CREATE SEQUENCE IF NOT EXISTS movie_id_seq START 1000;
    CREATE TABLE movies (
        movie_id INT DEFAULT nextval('movie_id_seq') PRIMARY KEY,
        movie_title TEXT NOT NULL,
        movie_release DATE,
        movie_genre TEXT,
        movie_rating REAL,
        movie_description TEXT
    );
    CREATE INDEX idx_movie_title ON movies (movie_title);
"""

sql_create_table_people = """
    CREATE SEQUENCE IF NOT EXISTS people_id_seq START 1000;
    CREATE TABLE people (
        people_id INT DEFAULT nextval('people_id_seq') PRIMARY KEY,
        people_name TEXT NOT NULL,
        people_role TEXT
    );
    CREATE INDEX idx_people_name ON people (people_name);
"""

sql_create_table_movie_people = """
    CREATE SEQUENCE IF NOT EXISTS mp_id_seq START 1000;
    CREATE TABLE movie_people (
        mp_id INT DEFAULT nextval('mp_id_seq') PRIMARY KEY,
        mp_movie_id INTEGER,
        mp_people_id INTEGER,
        FOREIGN KEY (mp_movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (mp_people_id) REFERENCES people(people_id)
    );
"""

sql_create_table_users = """
    CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1000;
    CREATE TABLE users (
        user_id INT DEFAULT nextval('user_id_seq') PRIMARY KEY,
        user_name TEXT NOT NULL,
        user_email TEXT NOT NULL,
        user_password TEXT NOT NULL
    );
"""

sql_create_table_reviews = """
    CREATE SEQUENCE IF NOT EXISTS review_id_seq START 1000;
    CREATE TABLE reviews (
        review_id INT DEFAULT nextval('review_id_seq') PRIMARY KEY,
        review_movie_id INTEGER,
        review_user_id INTEGER,
        review_text TEXT,
        review_date DATE,
        FOREIGN KEY (review_movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (review_user_id) REFERENCES users(user_id)
    );
"""

sql_create_table_news = """
    CREATE TABLE news (
        news_id SERIAL PRIMARY KEY,
        news_title TEXT,
        news_content TEXT,
        news_author TEXT,
        news_publish DATE
    );
"""

sql_create_view_people_movie = """
    CREATE OR REPLACE VIEW people_movie_view AS
        SELECT p.people_name, p.people_role, m.movie_title, m.movie_id
        FROM people p
        JOIN movie_people ON p.people_id = movie_people.mp_people_id
        JOIN movies m ON movie_people.mp_movie_id = m.movie_id
        ORDER BY p.people_name;
"""

sql_create_view_movie_details = """
    CREATE OR REPLACE VIEW movie_details_view AS
        SELECT m.movie_id, m.movie_title, m.movie_release, m.movie_genre, m.movie_rating, m.movie_description, 
        STRING_AGG(p.people_name || ' (' || p.people_role || ')', ', ') AS Cast
        FROM movies m
        JOIN movie_people mp ON m.movie_id = mp.mp_movie_id
        JOIN people p ON mp.mp_people_id = p.people_id
        GROUP BY m.movie_id
        ORDER BY m.movie_title;
"""

sql_create_function_add_movie_with_people = """
    CREATE OR REPLACE FUNCTION add_movie_with_people(
        my_title TEXT, 
        my_release DATE, 
        my_genre TEXT, 
        my_rating REAL, 
        my_description TEXT, 
        new_people TEXT[]) 
        RETURNS INTEGER 
    AS $$
    DECLARE
        new_movie_id INTEGER;
        new_people_id INTEGER;
    BEGIN
        -- Добавляем новый фильм
        INSERT INTO movies (movie_title, movie_release, movie_genre, movie_rating, movie_description)
        VALUES (my_title, my_release, my_genre, my_rating, my_description)
        RETURNING movie_id INTO new_movie_id;
    
        -- Добавляем связанных с фильмом актеров
        FOR i IN 1..array_length(new_people, 1) LOOP
            
            INSERT INTO people (people_name, people_role) 
            VALUES (new_people[i][1], new_people[i][2])
            RETURNING people_id INTO new_people_id;
    
            INSERT INTO movie_people (mp_movie_id, mp_people_id)
            VALUES (new_movie_id, new_people_id);
    
        END LOOP;
        RETURN new_movie_id;
    END;
    $$ LANGUAGE plpgsql;
"""
