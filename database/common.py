import sqlite3
from sqlite3 import Connection
from typing import Dict, List, NoReturn

CREATE_TABLES = """
drop table if exists users;
create table users (
    user_id integer primary key autoincrement,
    telegram_user_id varchar(50) not null
);

drop table if exists queries;
create table queries (
    query_id integer primary key autoincrement,
    command text not null,
    city text not null,
    day_in text not null,
    day_out text not null,
    min_price text default null, 
    max_price text default null,
    user_id integer references users(user_id)
);

drop table if exists results;
create table results (
    result_id integer primary key autoincrement,
    hotel_name text not null,
    rate text,
    address text not null,
    price text not null,
    query_id integer references queries(query_id)
)
"""

def generate_db() -> NoReturn:
    """
    Создание базы данных
    """
    with sqlite3.connect("telebot.db") as conn:
        cursor = conn.cursor()
        #cursor.executescript(CREATE_TABLES)
        conn.commit()


def get_user_id(telegram_id: str, conn: Connection) -> str:
    """
    Получение id пользователя по его telegram_id. Если пользователя нет в базе данных, его добавление.

    @param telegram_id: Id пользователя в Telegram
    @param conn: SQLite объект подключения к базе данных.
    @return: id пользователя
    """
    cursor = conn.cursor()
    cursor.execute("select user_id from users "
                   "where telegram_user_id = ?", (telegram_id,))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("insert into users(telegram_user_id) "
                       "values(?);", (telegram_id,))
        conn.commit()
        return str(cursor.lastrowid)
    else:
        return data[0][0]


def add_results(results: List[Dict], query_id: int, conn: Connection) -> NoReturn:
    """
    Добавление результатов запроса в базу данных
    """
    cursor = conn.cursor()
    results = [(result.get('name'), result.get('rate'),
                result.get('address'), result.get('price'), query_id)
               for result in results]
    cursor.executemany('''insert into results(hotel_name, rate, 
                            address, price, query_id) 
                          values(?, ?, ?, ?, ?)''', results)


def add_to_db(data: Dict[str, str], result: List[Dict]) -> NoReturn:
    """
    Добавление полной информации о запросе в базу данных
    """
    with sqlite3.connect("telebot.db") as conn:
        query_id = add_query(data=data, conn=conn)
        add_results(results=result, query_id=query_id, conn=conn)


def add_query(data: Dict[str, str], conn: Connection) -> int:
    """
    Добавление запроса в базу данных

    @param data: Информация о запросе:
    - Введенная команда
    - Город
    - Дата въезда в отель
    - Дата выезда из отеля
    """
    user_id = get_user_id(data.get('user_id'), conn)
    cursor = conn.cursor()
    cursor.execute("insert into queries(command, city, "
                   "day_in, day_out, min_price, max_price, user_id)"
                   " values(?, ?, ?, ?, ?, ?, ?);",
                   (data.get('command'), data.get('city'),
                    data.get('day_in'), data.get('day_out'),
                    data.get('min_price'), data.get('max_price'), user_id))
    conn.commit()
    return cursor.lastrowid


def get_history(user_id: str, limit: int) -> List[Dict]:
    """
    Получение истории запросов

    @param user_id: Telegram-id пользователя
    @param limit: Число запросов, выведенных пользователю
    @return: Список запросов в количестве limit пользователя с id user_id
    """
    with sqlite3.connect("telebot.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''select command, city, day_in, day_out, 
                          min_price, max_price, query_id from queries
                          left join users on users.user_id = queries.user_id
                          where telegram_user_id = ?
                          limit ?;''', (user_id, limit))
        queries = [dict(q) for q in cursor.fetchall()]
        for query in queries:
            cursor.execute('''select hotel_name, rate, 
                              address, price from results
                              left join queries q on q.query_id = results.query_id
                              where q.query_id = ?;''', (query.get('query_id'),))
            results = [dict(i) for i in cursor.fetchall()]
            query['results'] = results
        return queries
