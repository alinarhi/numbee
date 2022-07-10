import logging

import config
from bot import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.choice_buttons import lang_choice, level_choice
from states import Level
from . import base_level, advanced_level


@dp.message_handler(commands="start", state='*')
async def start_working(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(text="Привет! Я NumBee - твой помощник в изучении чисел на разных языках :)")
    await Level.NONE.set()
    await send_help(message)


@dp.message_handler(commands="help", state='*')
async def send_help(message: Message):
    await message.answer(
"""
Я могу быть твоим наставником в изучении 6 языков!

Чтобы увидеть доступные команды, начни писать / или загляни в меню команд

У нас есть 3 уровня обучения:

Нулевой - для запоминания произношения: ты отправляешь мне числа - я показываю, как их произносить.

Базовый - начинаем практиковаться: задания на произношение или аудирование.

Продвинутый - подключаем математику: устно решаем простые арифметические примеры
"""
)


@dp.message_handler(commands="stop", state='*')
async def stop_level(message: Message, state: FSMContext):
    level = await state.get_state()
    data = await state.get_data()
    if level != None and level != 'Level:NONE':
        if level != 'Level:ZERO':
            await message.answer(f"Всего ошибок: {data['mistakes']} из {data['total']}")
        await Level.NONE.set()
        logging.info(f"USER: {message.from_user.username} set state: {await state.get_state()}")
        await message.answer("Уровень завершен!")


@dp.message_handler(commands="lang", state=Level.NONE)
async def choose_lang(message: Message):
    await message.answer(text = "Выбери язык:", reply_markup=lang_choice)


@dp.callback_query_handler(text_contains="lang", state=Level.NONE)
async def set_lang(call: CallbackQuery, state: FSMContext):
    call_data = call.data.split(":")
    await state.update_data(lang=call_data[1])
    logging.info(f"USER: {call.from_user.username} set lang: {call_data[1]}")
    await call.message.answer(f"Отлично! Будем учить {call_data[2]}")
    await call.answer(cache_time=30)
    await call.message.delete()
    await choose_level(call.message)


@dp.message_handler(commands="level", state=Level.NONE)
async def choose_level(message: Message):
    await message.answer(text = '''Выбери уровень: 
    
Нулевой: ты отправляешь мне числа - я показываю, как их произносить.
Базовый: задания на произношение или аудирование.
Продвинутый: арифметические примеры.''', reply_markup=level_choice)


@dp.callback_query_handler(text_contains="level", state=Level.NONE)
async def set_level(call: CallbackQuery, state: FSMContext):
    call_data = call.data.split(":")
    await call.message.answer(f"Запускаю {call_data[2]} уровень")
    await call.answer(cache_time=30)
    await call.message.delete()
    await state.update_data(total=-1)
    await state.update_data(mistakes=0)
    if (call_data[1]=="1"):
        await Level.BASE_START.set()
        await base_level.choose_mode(call.message)
    elif (call_data[1]=="0"):
        await Level.ZERO.set()
        await call.message.answer("Отправляй мне числа, и я покажу тебе, как их произносить")
    else:
        await Level.ADVANCED.set()
        await advanced_level.send_task(call.message, state)
    st = await state.get_state()
    logging.info(f"USER: {call.from_user.username} set state: {st}")


@dp.message_handler(state=Level.NONE)
async def answer(message: Message):
    await message.answer("Я бы с радостью побеседовал с тобой, но пока не умею :( Нажми /help, чтобы узнать, как со мной общаться")
