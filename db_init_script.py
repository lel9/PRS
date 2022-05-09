import csv, sqlite3

# функция удаления всех таблиц
def delete_all(conn):
    cur = conn.cursor()
    cur.executescript('drop table if exists movies;')
    cur.executescript('drop table if exists ratings;')
    cur.executescript('drop table if exists links;')
    cur.close()
    pass

# функция создания таблицы фильмов
def create_movies_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS movies(
            movieId INTEGER PRIMARY KEY,
            title TEXT,
            year INTEGER,
            genres TEXT);
        """)

# функция создания таблицы оценок
def create_ratings_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS ratings(
            userId INTEGER,
            movieId INTEGER,
            rating REAL,
            timestamp TIMESTAMP,
            FOREIGN KEY (movieId) REFERENCES movies (movieId));
        """)

# функция создания таблицы тегов
def create_tags_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS tags(
            userId INTEGER,
            movieId INTEGER,
            tag TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (movieId) REFERENCES movies (movieId));
        """)

# функция создания всех таблиц
def create_tables(conn):
    cur = conn.cursor()
    create_movies_table(cur)
    create_ratings_table(cur)
    create_tags_table(cur)
    conn.commit()
    cur.close()

# функция загрузки данных о фильмах из movies.csv
def load_movies_data(dir, conn):
    with open(dir + '/movies.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = []
        for i in dr:
            # если жанров нет, записываем пустую строку
            genres = i['genres'] if i['genres'] != '(no genres listed)' else ''
            if '(' in i['title']:
                # вытаскиваем из title название и год выхода фильма
                title, year = i['title'].rsplit('(', 1)
                try:
                    year = int(year.strip()[:-1])
                except:
                    year = None
                to_db.append((i['movieId'], title.strip(), year, genres))
            else:
                to_db.append((i['movieId'], title.strip(), None, genres))

    conn.executemany("INSERT INTO movies (movieId, title, year, genres) "
                     "VALUES (?, ?, ?, ?);", to_db)
    conn.commit()

# функция загрузки данных об оценках из ratings.csv
def load_ratings_data(dir, conn):
    with open(dir + '/tags.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['userId'], i['movieId'], i['tag'], i['timestamp'])
                 for i in dr]

    conn.executemany("INSERT INTO tags (userId, movieId, tag, timestamp) "
                     "VALUES (?, ?, ?, ?);", to_db)
    conn.commit()

# функция загрузки данных о тегах из tags.csv
def load_tags_data(dir, conn):
    with open(dir + '/ratings.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['userId'], i['movieId'], i['rating'], i['timestamp'])
                 for i in dr]

    conn.executemany("INSERT INTO ratings (userId, movieId, rating, timestamp) "
                     "VALUES (?, ?, ?, ?);", to_db)
    conn.commit()

# функция загрузки всех данных
def load_data(dir, conn):
    load_movies_data(dir, conn)
    load_ratings_data(dir, conn)
    load_tags_data(dir, conn)


conn = sqlite3.connect('ml.db')

delete_all(conn)
create_tables(conn)
load_data('ml-latest-small', conn)

conn.close()

