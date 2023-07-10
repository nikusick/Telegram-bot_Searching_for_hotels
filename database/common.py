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
    query_text text not null,
    user_id integer references users(user_id)
);
"""


def generate_db() -> NoReturn:
    """
    Создание базы данных
    """
    with sqlite3.connect("telebot.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES)
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
                       "values(?)", (telegram_id,))
        conn.commit()
        return get_user_id(telegram_id, conn)
    else:
        return data[0][0]


def add_query(data: Dict[str, str]) -> NoReturn:
    """
    Добавление запроса в базу данных
    ================================
    @param data: Информация о запросе:
    - Введенная команда
    - Город
    - Дата въезда в отель
    - Дата выезда из отеля
    """
    with sqlite3.connect("telebot.db") as conn:
        user_id = get_user_id(data.get('user_id'), conn)
        cursor = conn.cursor()
        cursor.execute("insert into queries(query_text, user_id) values(?, ?)",
                       (f'Команда: {data.get("command")}\n'
                        f'Город: {data.get("city")}\n'
                        f'Дата въезда: {data.get("day_in")}\n'
                        f'Дата выезда: {data.get("day_out")}\n', user_id))
        conn.commit()


def get_history(user_id: str, limit: int) -> List[str]:
    """
    Получение истории запросов
    @param user_id: Telegram-id пользователя
    @param limit: Число запросов, выведенных пользователю
    @return: Список запросов в количестве limit пользователя с id user_id
    """
    with sqlite3.connect("telebot.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select query_text from queries "
                       "left join users on users.user_id = queries.user_id "
                       "where telegram_user_id = ? "
                       "limit ?;", (user_id, limit))
        result = [query[0] for query in cursor.fetchall()]
        return result
