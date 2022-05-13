import logging
import random
import tempfile

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import types

import db
import utils
from bot import dp

from keyboards.inline.choice_buttons import base_mode_choice
from states import Base
from .str_consts import CORRECT_REPLIES, WRONG_REPLIES, UNRECOGNIZED


@dp.message_handler(commands="mode", state=Base)
async def choose_mode(message: Message):
    await message.answer(
        "Доступные режимы:\n\nПроизношение: я буду отправлять тебе число, а ты - произносить его в голосовом "
        "сообщении на выбранном языке.\n\nАудирование - я произношу число, а ты пишешь его цифрами.\n\n"
        "Случайный - чередование произношения и аудирования.\n\nВыбирай!",
        reply_markup=base_mode_choice)
    await Base.SET_MODE.set()


@dp.callback_query_handler(text_contains="mode", state=Base.SET_MODE)
async def set_mode(call: CallbackQuery, state: FSMContext):
    call_data = call.data.split(":")
    mode = call_data[1]
    await state.update_data(mode=mode)
    logging.info(f"USER: {call.from_user.username} set mode for base level: {mode}")
    await state.update_data(mistakes=0)
    await call.message.answer(f"Режим: {call_data[2]}")
    await choose_range(call.message)
    await call.answer(cache_time=30)
    await call.message.delete()


@dp.message_handler(commands="range", state=Base)
async def choose_range(message: Message):
    await message.answer("Введи два неотрицательных числа через пробел: это будет диапазон значений для изучения.\n"
                         + "Второе число должно быть больше! Пример:\n0 100")
    await message.answer("Если захочешь прервать уровень, напиши /stop")
    await Base.SET_RANGE.set()


@dp.message_handler(state=Base.SET_RANGE)
async def set_range(message: Message, state: FSMContext):
    users_range = message.text.split()
    if len(users_range) != 2:
        await message.reply("Мне нужно ровно 2 числа, напиши еще раз")
    else:
        try:
            l = int(users_range[0])
            r = int(users_range[1])
            if l < 0 or r < 0:
                await message.reply("Давай будем учить только неотрицательные числа, хорошо? Напиши еще раз")
            elif l >= r:
                await message.reply("Второе число должно быть больше первого!")
            else:
                await state.update_data(range=[l, r])
                await message.answer("Поехали!")
                await Base.PLAY.set()
                await send_number(message, state)
        except ValueError:
            await message.reply("Похоже, ты ввел не числа. Попробуй еще раз")


async def send_number(message: Message, state: FSMContext):
    data = await state.get_data()
    rng = data["range"]
    mode = data["mode"]
    total = data["total"]
    num = random.randint(rng[0], rng[1])
    await state.update_data(num=num)
    await state.update_data(total=total+1)
    if mode == "2":
        mode = str(random.randint(0, 1))
    if mode == "0":
        await message.answer(str(num))
    if mode == "1":
        fileid = await db.get_num(str(num), data["lang"])
        if fileid is None:
            file = utils.tts(str(num), data["lang"])
            reply = await message.answer_voice(open(file.name, "rb"))
            file.close()
            await db.add_num(str(num), data["lang"], reply.voice.file_id)
        else:
            await message.answer_voice(fileid)


@dp.message_handler(state=Base.PLAY, content_types=types.ContentType.VOICE)
async def check_voice(message: Message, state: FSMContext):
    file = tempfile.NamedTemporaryFile()
    data = await state.get_data()
    num = data["num"]
    mode = data["mode"]
    mistakes = data["mistakes"]
    if mode != "1":
        try:
            await message.voice.download(destination_file=file.name)
            text = utils.stt(file, data["lang"])
            ans = int(text)
            if ans != num:
                await message.reply(f"Мне послышалось, что ты произнес {ans}, а надо было {num}. Давай еще раз?")
                await state.update_data(mistakes=mistakes+1)
            else:
                await message.reply(CORRECT_REPLIES[random.randint(0, len(CORRECT_REPLIES) - 1)])
                await send_number(message, state)
        except ValueError:
            await message.reply(UNRECOGNIZED)
        finally:
            file.close()
    else:
        await message.answer("Тебе нужно было написать число, которое я произнес. Давай еще раз?"
                             "\nЕсли хочешь закончить уровень, пиши /stop")


@dp.message_handler(state=Base.PLAY, content_types=types.ContentType.TEXT)
async def check_text(message: Message, state: FSMContext):
    data = await state.get_data()
    num = data["num"]
    mode = data["mode"]
    mistakes = data["mistakes"]
    if mode != "0":
        try:
            ans = int(message.text)
            if ans != num:
                await message.reply(WRONG_REPLIES[random.randint(0, len(WRONG_REPLIES) - 1)])
                await state.update_data(mistakes=mistakes+1)
            else:
                await message.reply(CORRECT_REPLIES[random.randint(0, len(CORRECT_REPLIES) - 1)])
                await send_number(message, state)
        except ValueError:
            await message.answer("Тебе нужно написать число")
    else:
        await message.answer("Тебе нужно было произнести число, которое я отправил. Давай еще раз?"
                             "\nЕсли хочешь закончить уровень, пиши /stop")
