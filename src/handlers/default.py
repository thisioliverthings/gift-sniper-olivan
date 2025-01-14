from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.data import Text, Markup
from src.utils import DefaultUtils, CustomCall, CustomMessage
from src.states import PaymentsStates
from src.handlers.profile import profile_handler


rname = 'based'
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.bot.database.create_user(
        message.from_user.id
    )
    await message.answer(
        text=Text.start.format(user=DefaultUtils.remove_html_tags(message.from_user.full_name)),
        reply_markup=Markup.start
    )


@router.callback_query(F.data.split('|')[0] == 'back')
async def back_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    back_argument = call.data.split('|')[1]
    if back_argument == 'profile':
        await profile_handler(CustomCall(call))


@router.message(F.text == 'Отмена', StateFilter(PaymentsStates.wait_payment))
async def cancel_handler_invoice(message: Message, state: FSMContext):
    invoice_id = (await state.get_data())["invoice_id"]
    invoice_message_id = await message.bot.database.get_invoice_message_id(
        invoice_id, False
    )

    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=invoice_message_id
    )

    await state.clear()
    await start_handler(message)