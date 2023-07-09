import sqlite3

CREATE_TABLES = """
drop table if exists users;
create table users (
    user_id integer primary key autoincrement,
    telegram_user_id varchar(50) not null
);

drop table if exists queries;
create table queries (
    query_id integer primary key autoincrement,
    query_text text not null,
    user_id integer references users(user_id)
);
"""


def generate_db():
    with sqlite3.connect("telebot.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES)
        conn.commit()


def add_user(telegram_id, conn):
    cursor = conn.cursor()
    cursor.execute("select user_id from users where telegram_user_id = ?", (telegram_id,))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("insert into users(telegram_user_id) values(?)", (telegram_id,))
        conn.commit()
        return add_user(telegram_id, conn)
    else:
        return data[0][0]


def add_query(data):
    with sqlite3.connect("telebot.db") as conn:
        user_id = add_user(data.get('user_id'), conn)
        cursor = conn.cursor()
        cursor.execute("insert into queries(query_text, user_id) values(?, ?)",
                       (f'Команда: {data.get("command")}\nГород: {data.get("city")}\n'
                        f'Дата въезда: {data.get("day_in")}\n'
                        f'Дата выезда: {data.get("day_out")}\n', user_id))
        conn.commit()


def get_history(user_id, limit):
    with sqlite3.connect("telebot.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select query_text from queries "
                       "left join users on users.user_id = queries.user_id "
                       "where telegram_user_id = ? "
                       "limit ?;", (user_id, limit))
        result = [query[0] for query in cursor.fetchall()]
        return result
