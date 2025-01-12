from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
                            ReplyKeyboardMarkup, KeyboardButton

class Markup:
    start = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='👤 Профиль')],
        [KeyboardButton(text='ℹ️ Информация')],
    ], resize_keyboard=True)

    profile = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up')]
    ])