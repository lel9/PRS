import time
from model_helpers import *

# функция получения списка всех фильмов
def get_all_movies():
    conn = None
    try:
        conn = get_db_connection()
        # запрашиваем из базы данных все фильмы
        rows = conn.execute('SELECT * FROM movies').fetchall()
        # преобразуем объект Row в словарь
        movies = [row_to_movie(row) for row in rows]
    except:
        movies = []
    finally:
        # закрываем соединение
        close_connection(conn)
    return movies

# функция получения фильма по id
def get_movie(id):
    conn = None
    try:
        conn = get_db_connection()
        # ищем в базе данных фильм
        row = conn.execute("SELECT * FROM movies WHERE movieId = ?",
                           (id,)).fetchone()
        # преобразуем объект Row в словарь
        movie = row_to_movie(row)
    except:
        movie = {}
    finally:
        # закрываем соединение
        close_connection(conn)

    return movie


# функция получения всех оценок по ключам
# args -- словарь с ключами поиска (userId, movieId)
def get_ratings(args):
    conn = None
    try:
        conn = get_db_connection()
        rows = search_rows(args, 'ratings', conn)
        # преобразуем объект Row в словарь
        ratings = [row_to_raiting(row) for row in rows]
    except:
        ratings = []
    finally:
        # закрываем соединение
        close_connection(conn)
    return ratings

# функия добавления оценки
def add_rating(rating):
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO ratings (userId, movieId, rating, timestamp) "
                     "VALUES (?, ?, ?, ?);",
                     (rating["userId"], rating["movieId"], rating["rating"],
                      # если timestamp передан, берем его, иначе берем текущее время
                      rating["timestamp"] if "timestamp" in rating else int(time.time()))) \
            .fetchone()
        conn.commit()
    except:
        pass
    finally:
        # закрываем соединение
        close_connection(conn)

# функция получения всех тегов по ключам
# args -- словарь с ключами поиска (userId, movieId)
def get_tags(args):
    conn = None
    try:
        conn = get_db_connection()
        rows = search_rows(args, 'tags', conn)
        # преобразуем объект Row в словарь
        tags = [row_to_tag(row) for row in rows]
    except:
        tags = []
    finally:
        # закрываем соединение
        close_connection(conn)
    return tags

# функция добавления тега
def add_tag(tag):
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO tags (userId, movieId, tag, timestamp) "
                     "VALUES (?, ?, ?, ?);",
                     (tag["userId"], tag["movieId"], tag["tag"],
                      # если timestamp передан, берем его, иначе берем текущее время
                      tag["timestamp"] if "timestamp" in tag else int(time.time())))\
            .fetchone()
        conn.commit()
    except:
        pass
    finally:
        # закрываем соединение
        close_connection(conn)


# функция поиска по заданным ключам
# args -- словарь ключей (userId и/или movieId)
# table_name -- таблица (ratings или tags)
# conn -- соединение с базой данных
def search_rows(args, table_name, conn):
    if table_name not in ["ratings", "tags"]:
        return None

    # берем ключ userId, если он есть
    userId = args['userId'] if 'userId' in args else None
    # берем ключ movieId, если он есть
    movieId = args['movieId'] if 'movieId' in args else None

    # если есть оба ключа
    if userId and movieId:
        # ищем в базе данных по двум ключам
        rows = conn.execute('SELECT * FROM ' + table_name + ' '
                            'WHERE userId = ? and movieId = ?',
                            (userId, movieId,)).fetchall()

    # если есть только ключ userId
    elif userId:
        # ищем в базе данных по ключу userId
        rows = conn.execute('SELECT * FROM ' + table_name + ' '
                            'WHERE userId = ?',
                            (userId,)).fetchall()

    # если есть только ключ movieId
    elif movieId:
        # ищем в базе данных по ключу movieId
        rows = conn.execute('SELECT * FROM ' + table_name + ' '
                            'WHERE movieId = ?',
                            (movieId,)).fetchall()

    # если нет ни одного ключа
    else:
        # запрашиваем из базы данных все строки таблицы
        rows = conn.execute('SELECT * FROM ' + table_name).fetchall()

    return rows
