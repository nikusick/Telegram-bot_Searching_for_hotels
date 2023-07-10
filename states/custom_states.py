from telebot.handler_backends import State, StatesGroup


class CustomStates(StatesGroup):
    city = State()  # Ожидание ввода города
    min_price = State()  # Ожидание ввода минимальной цены
    max_price = State()  # Ожидание ввода максимальной цены
    count_of_notes = State()  # Ожидание ввода количества искомых номеров
    day_in = State()  # Ожидание ввода дня въезда
    day_out = State()  # Ожидание ввода дня выезда
