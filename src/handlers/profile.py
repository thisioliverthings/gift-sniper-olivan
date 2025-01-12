from aiogram import Router, F
from aiogram.types import Message

from src.data import Text, Markup
from src.utils import DefaultUtils


rname = 'based'
router = Router()


@router.message(F.text == '👤 Профиль')
async def start_handler(message: Message):
    await message.answer(
        text=Text.start.format(user=DefaultUtils.remove_html_tags(message.from_user.full_name)),
        reply_markup=Markup.start
    )