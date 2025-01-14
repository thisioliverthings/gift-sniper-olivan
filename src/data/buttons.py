from typing import Tuple, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
                            ReplyKeyboardMarkup, KeyboardButton

class Markup:
    start = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='👤 Профиль')],
        [KeyboardButton(text='ℹ️ Информация')],
    ], resize_keyboard=True)

    profile = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up')],
        [InlineKeyboardButton(text='🚀 Приобрести VIP', callback_data='buy_vip')]
    ])

    cancel_invoice = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отмена')]
    ], resize_keyboard=True)

    @staticmethod
    def back(back_type: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back|{back_type}')

    @staticmethod
    def configurator(*buttons: Tuple[List[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=list(buttons))