from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    get_user = State()
    delete_messages = State()


class KeywordsState(StatesGroup):
    show_keywords = State()
    add_keyword = State()
    delete_keyword = State()
