import sqlite3

# вспомогательные функции

# функция создания соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('ml.db')
    conn.row_factory = sqlite3.Row
    return conn

# функция закрытия соединения с базой данных
def close_connection(conn):
    if conn != None:
        conn.close()

# функция преобразования объекта Row в словарь (для фильмов)
def row_to_movie(row):
    movie = {}
    movie["movieId"] = row["movieId"]
    movie["title"] = row["title"]
    movie["year"] = row["year"]
    movie["rating"] = row["rating"]
    # если жанров нет (пустая строка), содаём пустой список
    movie["genres"] = row["genres"].split('|') if row["genres"] else []
    return movie

# функция преобразования объекта Row в словарь (для оценок)
def row_to_raiting(row):
    rating = {}
    rating["userId"] = row["userId"]
    rating["movieId"] = row["movieId"]
    rating["rating"] = row["rating"]
    rating["timestamp"] = row["timestamp"]
    return rating

# функция преобразования объекта Row в словарь (для тегов)
def row_to_tag(row):
    tag = {}
    tag["userId"] = row["userId"]
    tag["movieId"] = row["movieId"]
    tag["tag"] = row["tag"]
    tag["timestamp"] = row["timestamp"]
    return tag
