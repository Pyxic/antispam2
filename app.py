# bot = Bot(token=TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)


from aiogram import executor

from loader import dp
import handlers


if __name__ == '__main__':
    executor.start_polling(dp)
