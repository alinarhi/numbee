from aiogram.dispatcher.filters.state import StatesGroup, State


class Level(StatesGroup):
    NONE = State()
    ZERO = State()
    ADVANCED = State()
    BASE = State()


class Base(StatesGroup):
    SET_MODE = State()
    SET_RANGE = State()
    PLAY = State()


