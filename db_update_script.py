import sqlite3

# функция добавления нового столбца (лаб. 1.2)
def add_rating_column(conn):
    cur = conn.cursor()
    cur.execute("""ALTER TABLE movies ADD rating REAL;""")
    conn.commit()
    cur.close()

# функция расчета среднего рейтинга фильма и сохранения его в столбец ratings
def load_rating(conn):
    cur = conn.cursor()
    cur.execute("""UPDATE movies SET rating = 
                     (SELECT AVG(rating) FROM ratings
                     WHERE ratings.movieId = movies.movieId);""")
    conn.commit()
    cur.close()

conn = sqlite3.connect('ml.db')

try:
    add_rating_column(conn)
except sqlite3.OperationalError as e:
    print(e)

load_rating(conn)

conn.close()