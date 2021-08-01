from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from settings import admin_id

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='настроить ключевые слова'),
            #KeyboardButton(text='статистика'),
        ],
        [
            KeyboardButton(text='удалить сообщения пользователя'),
        ],
        [
            KeyboardButton(text='удаление по ключевым словам'),
        ],
        [
            KeyboardButton(text='закрыть меню'),
        ]
    ],
    resize_keyboard=True,
)


keywords_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вывести слова', callback_data="show_keywords"),
        ]
    ]
)

keywords_menu_level2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить слово", callback_data="add_keyword"),
            InlineKeyboardButton(text='Удалить слово', callback_data="delete_keyword"),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ]
    ]
)
