from typing import Tuple, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
                            ReplyKeyboardMarkup, KeyboardButton

class Markup:
    # قائمة البداية
    start = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='👤 الملف الشخصي')],
        [KeyboardButton(text='ℹ️ المعلومات')],
    ], resize_keyboard=True)

    # قائمة الملف الشخصي
    profile = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='شحن الرصيد', callback_data='top_up')],
        [InlineKeyboardButton(text='🚀 شراء VIP', callback_data='buy_vip')]
    ])

    # زر إلغاء الفاتورة
    cancel_invoice = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='إلغاء')]
    ], resize_keyboard=True)

    # زر شراء VIP للأبد
    buy_vip = InlineKeyboardButton(
        text='شراء للأبد', callback_data='invoice_buy_vip'
    )

    @staticmethod
    def setting_generator(mode: int) -> InlineKeyboardMarkup:
        is_active = lambda _mode: '✅' if mode == _mode else ''
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f'{is_active(0)} على كامل الرصيد', callback_data='dev')],
                [InlineKeyboardButton(text=f'{is_active(1)} نسبة من الرصيد', callback_data='dev')],
                [InlineKeyboardButton(text=f'{is_active(2)} حد النجوم', callback_data='dev')],
                [Markup.back('info')]
            ]
        )

    @staticmethod
    def settings(admin_url: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='الإعدادات', callback_data='settings')],
        [InlineKeyboardButton(text='🖥 الإدارة', url=admin_url)]
    ])

    @staticmethod
    def back(back_type: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text='⬅️ رجوع', callback_data=f'back|{back_type}')

    @staticmethod
    def configurator(*buttons: Tuple[List[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=list(buttons))