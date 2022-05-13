import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

import db
from config import *

bot = Bot(token=BOT_TOKEN)
storage = RedisStorage2(REDIS_HOST, REDIS_PORT)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=storage)

commands = [
        BotCommand(command="/help", description="О боте"),
        BotCommand(command="/lang", description="Выбрать язык обучения"),
        BotCommand(command="/level", description="Выбрать уровень обучения"),
        BotCommand(command="/stop", description="Завершить текущий уровень")
    ]


async def on_start(dispatcher):
    await bot.set_my_commands(commands)
    await bot.send_message(chat_id=ADMIN_ID, text='bot started')
    import db
    db.connect()


async def on_shutdown(dispatcher):
    try:
        await bot.send_message(chat_id=ADMIN_ID, text='bot stopped')
        db.close()
        await dp.storage.close()
        await dp.storage.wait_closed()
    finally:
        await (await bot.get_session()).close()


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown)

