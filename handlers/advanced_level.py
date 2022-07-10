import random
import tempfile

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram import types

import utils
from bot import dp

from states import Level
from .str_consts import CORRECT_REPLIES, WRONG_REPLIES, OPERATIONS, UNRECOGNIZED


async def send_task(message: Message, state: FSMContext):
    oper = OPERATIONS[random.randint(0, len(OPERATIONS) - 1)]
    if oper == '\u00d7':
        first = random.randint(1, 20)
        second = random.randint(1, 10)
        ans = first*second
    else:
        first = random.randint(1, 100)
        second = random.randint(1, 100)
    expr = str(max(first, second)) + oper + str(min(first, second))
    data = await state.get_data()
    if oper == '+':
        ans = first + second
    elif oper == '\u2212':
        ans = abs(first - second)
    await state.update_data(num=ans)
    file = utils.tts(expr, data["lang"])
    await message.answer_voice(open(file.name, "rb"))
    file.close()
    await state.update_data(total=data["total"]+1)


@dp.message_handler(state=Level.ADVANCED, content_types=types.ContentType.VOICE)
async def check_ans(message: Message, state: FSMContext):
    file = tempfile.NamedTemporaryFile()
    data = await state.get_data()
    num = data["num"]
    try:
        await message.voice.download(destination_file=file.name)
        text = utils.stt(file, data["lang"])
        ans = int(text)
        if ans != num:
            await message.reply(WRONG_REPLIES[random.randint(0, len(WRONG_REPLIES) - 1)])
            await state.update_data(mistakes=data["mistakes"]+1)
        else:
            await message.reply(CORRECT_REPLIES[random.randint(0, len(CORRECT_REPLIES) - 1)])
            await send_task(message, state)
    except ValueError:
        await message.reply(UNRECOGNIZED)
    finally:
        file.close()
