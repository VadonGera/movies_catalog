import psycopg2
from config import host, user, password, db_name, port

db_params = {
    "host": host,
    "user": user,
    "password": password,
    "database": db_name,
    "port": port
}


def connect_database():
    with psycopg2.connect(**db_params) as connection:
        connection.autocommit = False
        return connection
