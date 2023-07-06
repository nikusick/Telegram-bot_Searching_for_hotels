from telebot.handler_backends import State, StatesGroup


class LowStates(StatesGroup):
    city = State()
    count_of_notes = State()
    day_in = State()
    day_out = State()


class HighStates(StatesGroup):
    city = State()
    count_of_notes = State()
    day_in = State()
    day_out = State()


class CustomStates(StatesGroup):
    city = State()
    low_price = State()
    high_price = State()
    count_of_notes = State()
    day_in = State()
    day_out = State()
