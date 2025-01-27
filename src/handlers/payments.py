from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from src.data import Text, Markup
from src.states import PaymentsStates
from src.utils import BalanceOperation, CRYPTO_BOT_USERNAME


rname = 'payments'
router = Router()


@router.callback_query(F.data == 'top_up')
async def new_top_up_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    back_message = await call.message.answer_photo(
        photo=FSInputFile(f'src/images/sendstars.jpg'),
        caption=Text.get_amount, 
        reply_markup=Markup.configurator([Markup.back('profile')])
    )
    await state.set_state(PaymentsStates.get_amount)
    await state.set_data({
        "back_mess_id": back_message.message_id
    })



@router.message(StateFilter(PaymentsStates.get_amount))
async def get_result(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.bot.delete_message(
        chat_id=message.chat.id, 
        message_id=data['back_mess_id']
    )

    if (
        message.reply_markup 
        and message.reply_markup.inline_keyboard[0][0].callback_data == 'check-creating'
        and message.via_bot.username == CRYPTO_BOT_USERNAME
    ):
        _message =  await message.reply(
            text=Text.wait_creating
        )
        await state.set_state(PaymentsStates.wait_payment)
        await state.set_data({
            "back_mess_id": _message.message_id
        })
        return

    await message.answer(
        text=Text.utils.bool_to_emoji(False), 
        reply_markup=Markup.start
    )
    await state.clear()


@router.edited_message(StateFilter(PaymentsStates.wait_payment))
async def process_edited_message(message: Message, state: FSMContext):
    print(message)


@router.pre_checkout_query(StateFilter(PaymentsStates.wait_payment))
async def process_pre_checkout_query(pre_checkout_query):
    is_pending = await pre_checkout_query.bot.database.is_invoice_pending(
        int(pre_checkout_query.invoice_payload)
    )
    
    if is_pending:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(
            ok=False,
            error_message=Text.errors.invoice_reject
        )


@router.message(F.successful_payment, StateFilter(PaymentsStates.wait_payment))
async def process_successful_payment(message: Message, state: FSMContext):
    invoice_id = int(message.successful_payment.invoice_payload)
    back_message_id = await message.bot.database.get_invoice_message_id(invoice_id, True)

    await message.bot.database.update_balance(
        message.from_user.id, 
        message.successful_payment.total_amount,
        operation=BalanceOperation.ADD
    )

    await message.bot.delete_message(
        chat_id=message.chat.id, 
        message_id=back_message_id
    )
    
    await message.answer(
        text=Text.success_invoice_emoji, 
        reply_markup=Markup.start
    )
    await message.answer(
        text=Text.successful_invoice,
        reply_markup=Markup.configurator([Markup.back('profile')])
    )
    
    await state.clear()


@router.callback_query(F.data == 'buy_vip')
async def vip_info_handler(call: CallbackQuery):
    await call.message.edit_text(
        text=Text.vip_text.format(call.bot.config.vip_price),
        reply_markup=Markup.configurator(
            [Markup.buy_vip],
            [Markup.back('profile')]
        )
    )


@router.callback_query(F.data == 'invoice_buy_vip')
async def vip_buy_handler(call: CallbackQuery):
    user_db = await call.bot.database.get_user(call.from_user.id)
    
    if user_db.vip:
        return await call.answer(
            text=Text.errors.already_buy, show_alert=True
        )

    if user_db.balance < call.bot.config.vip_price:
        return await call.answer(
            text=Text.errors.insufficient_funds,
            show_alert=True
        )
    
    await call.bot.database.update_balance(
        call.from_user.id, 
        call.bot.config.vip_price,
        operation=BalanceOperation.SUBTRACT
    )
    await call.bot.database.grant_vip(call.from_user.id, True)
    
    await call.message.edit_text(
        text=Text.success_buy_vip,
        reply_markup=Markup.configurator(
            [Markup.back('profile')]
        )
    )