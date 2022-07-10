from aiogram.dispatcher.filters.state import StatesGroup, State


class Level(StatesGroup):
    NONE = State()
    ZERO = State()
    BASE = State()
    BASE_SET_MODE = State()
    BASE_SET_RANGE = State()
    BASE_START = State()
    BASE_LISTENING = State()
    BASE_PRONOUNCING = State()
    ADVANCED = State()
