from telebot.handler_backends import State, StatesGroup


class CustomStates(StatesGroup):
    city = State()
    min_price = State()
    max_price = State()
    count_of_notes = State()
    day_in = State()
    day_out = State()
