from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# gtts-cli --all

lang_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Английский", callback_data="lang:en:английский"),
            InlineKeyboardButton(text="Немецкий", callback_data="lang:de:немецкий")
        ],
        [
            InlineKeyboardButton(text="Испанский", callback_data="lang:es:испанский"),
            InlineKeyboardButton(text="Французский", callback_data="lang:fr:французский")
        ],
        [
            InlineKeyboardButton(text="Китайский", callback_data="lang:zh:китайский"),
            InlineKeyboardButton(text="Японский", callback_data="lang:ja:японский")
        ],

    ]
)

level_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Нулевой", callback_data="level:0:нулевой")
        ],
        [
            InlineKeyboardButton(text="Базовый", callback_data="level:1:базовый")
        ],
        [
            InlineKeyboardButton(text="Продвинутый", callback_data="level:2:продвинутый")
        ]
    ]
)

base_mode_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Произношение", callback_data="mode:0:произношение")
        ],
        [
            InlineKeyboardButton(text="Аудирование", callback_data="mode:1:аудирование")
        ],
        [
            InlineKeyboardButton(text="Случайный", callback_data="mode:2:случайный")
        ]
    ]
)