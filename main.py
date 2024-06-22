from datetime import datetime
from database.creation import create_database
from database.requests import (
    get_movies_all, get_movies_select, get_cast_list, add_new_movie, update_rating_movie,
    add_movie_with_people, get_people_movie, delete_movie, search_movies_person, get_movies_details
)

if __name__ == '__main__':
    # Создаем базу данных
    create_database()

    # Список всех фильмов
    for movie in get_movies_all():
        print(movie)

    # Список всех фильмов c актерами и создателями через представление
    for movie in get_movies_details():
        print(movie)

    # Поиск фильмов по рейтингу и дате релиза
    for movie in get_movies_select(8.1, 2000):
        print(movie)

    # Список актеров и их ролей в конкретном фильме id
    for person in get_cast_list(1):
        print(person)

    # Добавление нового фильма
    new_movie = ("Титаник", "1997-11-01", "драма", 7.4, "Ничто на Земле не сможет разлучить их")
    new_id = add_new_movie(new_movie)
    print("id нового фильма:", new_id)

    # Обновляем рейтинг фильма
    my_movie = update_rating_movie(new_id, 7.9)
    print(f"Изменили рейтинг фильма {my_movie[0]} на {my_movie[1]}")

    # Удаление фильма по id
    del_id = delete_movie(new_id)
    print("Удалили фильм с id:", del_id)

    # Добавление нового фильма вместе со списком актеров
    movie = (
        'Послезавтра',
        datetime.strptime("2004-05-17", "%Y-%m-%d").date(),
        'фантастика, триллер, драма, приключения',
        7.7,
        'Where will you be?'
    )
    person_1 = ('Джейк Джилленхол', 'актер')
    person_2 = ('Роланд Эммерих', 'режиссер')
    person_3 = ('Села Уорд', 'актер')
    people = (list(person_1), list(person_2), list(person_3))

    new_movie_id = add_movie_with_people(movie, people)

    # Проверяем персон, которых добавили с новым фильмом через представление
    for person in get_people_movie(new_movie_id):
        print(person)

    # Поиск фильмов по части имени актеров и авторов
    for movie in search_movies_person('макконах'):
        print(movie)
