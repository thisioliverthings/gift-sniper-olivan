from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.data import Text, Markup
from src.config import Config
from src.utils import DefaultUtils, CustomCall, CustomMessage
from src.states import PaymentsStates
from src.data.database import Database


rname = 'info'
router = Router()


@router.message(F.text == 'ℹ️ معلومات')
async def info_handler(message: Message):
    config: Config = message.bot.config
    user = await message.bot.database.get_user(
        message.from_user.id
    )

    await message.answer(
        text=Text.info.format(
            startup_date=message.bot.starup_date,
            user_count=await message.bot.database.get_user_count(),
            storage=await message.bot.database.get_total_balance(),
            all_buy=await message.bot.database.get_total_gifts(),
            interval=config.vip_poll_interval if user.vip else config.default_poll_interval
        ), reply_markup=Markup.settings(config.admin_url)
    )


@router.callback_query(F.data == 'settings')
async def settings_handler(call: CallbackQuery):
    user = await call.bot.database.get_user(
        call.from_user.id
    )
    await call.message.edit_text(
        text=Text.info_setting,
        reply_markup=Markup.setting_generator(user.buying_mode)
    )