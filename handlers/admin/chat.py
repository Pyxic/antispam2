from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import Throttled, MessageToDeleteNotFound
from keyboards import menu, keywords_menu
from loader import dp, bot
from models import Keywords, Chat
from settings import admin_id, bot_id
from states.add_chat import Test, KeywordsState


async def anti_flood(*args, **kwargs):
    m = args[0]
    username = m['from']['username']
    await bot.send_message(bot_id, f"Пользователь {username} флудит в чате {m.chat.title}")
    await bot.delete_message(m.chat.id, m.message_id)


def auth(func):
    async def wrapper(message: types.Message):
        if str(message['from']['id']) not in admin_id:
            return await message.reply("Доступ запрещен", reply=False)
        return await func(message)
    return wrapper


def has_keywords(func):
    async def wrapper(message: types.Message):
        if Keywords.has_keyword(message.text):
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(bot_id, f"Пользователь {message['from']['username']} отправил "
                                           f"сообщение с запрещенными словами")
            return await message.reply("Сообщение имеет запрещенные слова", reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет!\nЭто бот для фильтра чата!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    print(message.chat.id)
    await message.answer("Помошь")


@dp.message_handler(text='настроить ключевые слова', state=None)
async def print_keywords_menu(message: types.Message):
    await message.answer("Ключевые слова", reply_markup=keywords_menu)


@dp.callback_query_handler(text_contains="show_keywords")
async def show_keyword(call: CallbackQuery):
    keywords = ', '.join([keyword.word for keyword in Keywords.select(Keywords.word)])
    await call.message.answer(keywords)


@dp.callback_query_handler(text_contains="add_keyword", state=None)
async def add_keyword(call: CallbackQuery):
    await call.message.answer("Ведите ключевое слово, которое хотите добавить")
    await KeywordsState.add_keyword.set()


@dp.message_handler(state=KeywordsState.add_keyword)
async def add_keyword_to_db(message: types.Message, state: FSMContext):
    Keywords.create(word=message.text)
    await message.answer("Ключевое слово добавлено")
    await state.finish()


@dp.callback_query_handler(text_contains="delete_keyword", state=None)
async def add_keyword(call: CallbackQuery):
    await call.message.answer("Ведите ключевое слово, которое хотите удалить")
    await KeywordsState.delete_keyword.set()


@dp.message_handler(state=KeywordsState.delete_keyword)
async def delete_keyword_from_db(message: types.Message, state: FSMContext):
    Keywords.delete().where(Keywords.word == message.text).execute()
    await message.answer("Ключевое слово удалено")
    await state.finish()


@dp.message_handler(text=['удалить сообщения пользователя'], state=None)
async def enter_user(message: types.Message):
    await message.answer("Введите имя пользователя у которого нужно удалить сообщения")
    await Test.delete_messages.set()


@dp.message_handler(text='настроить антиспам')


@dp.message_handler(state=Test.delete_messages)
async def delete_messages_by_user(message: types.Message, state: FSMContext):
    print('delete')
    messages = Chat.select().where(Chat.username == message.text)
    for mes in messages:
        try:
            await bot.delete_message(mes.chat_id, mes.message_id)
        except MessageToDeleteNotFound:
            continue
    count = Chat.delete().where(Chat.username == message.text).execute()
    if count == 0:
        await message.answer("Сообщений пользователя не найдено")
    await state.finish()


@dp.message_handler(text="удаление по ключевым словам")
async def delete_messages_by_keywords(message: types.Message):
    messages = Chat.select()
    keywords = [row.word for row in Keywords.select(Keywords.word)]
    for mes in messages:
        for keyword in keywords:
            if keyword in mes.text:
                try:
                    await bot.delete_message(mes.chat_id, mes.message_id)
                    Chat.delete().where(Chat.id == mes.id).execute()
                except MessageToDeleteNotFound:
                    Chat.delete().where(Chat.id == mes.id).execute()
                    continue
    count = Chat.delete().where(Chat.username == message.text).execute()
    if count < 1:
        await message.answer("Сообщений не найдено")
    

@dp.message_handler(user_id=admin_id, commands='admin')
@auth
async def process_help_command(message: types.Message):
    await message.answer("Админ", reply_markup=menu)


@dp.message_handler()
@has_keywords
@dp.throttled(anti_flood, rate=1/2)
async def process_message(message: types.Message):
    chat = Chat.create(chat_id=message.chat.id, username=message['from']['username'], message_id=message.message_id,
                       text=message.text)
    print(chat)
    print(message)
