from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import utils
import db
from bot import dp
from states import Level


@dp.message_handler(state=Level.ZERO)
async def zero_level(message: Message, state: FSMContext):
    try:
        num = int(message.text)
        data = await state.get_data()
        fileid = await db.get_num(message.text, data["lang"])
        if fileid is None:
            file = utils.tts(message.text, data["lang"])
            reply = await message.reply_voice(open(file.name, "rb"))
            file.close()
            await db.add_num(message.text, data["lang"], reply.voice.file_id)
        else:
            await message.reply_voice(fileid)
    except ValueError:
        await message.answer("Я умею озвучивать только числа :(\nПожалуйста, отправь число")
