from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductState(StatesGroup):
    name = State()
