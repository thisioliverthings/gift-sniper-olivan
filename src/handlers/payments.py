from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

from src.data import Text, Markup
from src.states import PaymentsStates
from src.utils import BalanceOperation


rname = 'payments'
router = Router()


@router.callback_query(F.data == 'top_up')
async def new_top_up_handler(call: CallbackQuery, state: FSMContext):
    back_message = await call.message.edit_text(
        text="💰 الرجاء إدخال المبلغ الذي تريد شحنه:", 
        reply_markup=Markup.configurator([Markup.back('profile')])
    )
    await state.set_state(PaymentsStates.get_amount)
    await state.set_data({
        "back_mess_id": back_message.message_id
    })


@router.message(StateFilter(PaymentsStates.get_amount))
async def create_invoice(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.bot.delete_message(
        chat_id=message.chat.id, 
        message_id=data['back_mess_id']
    )

    if not message.text.isnumeric():
        return await message.answer(
            text="⚠️ الرجاء إدخال رقم صحيح.",
            reply_markup=Markup.configurator([Markup.back('profile')])
        )

    await message.answer(
        text="💳 جاري إنشاء الفاتورة...",
        reply_markup=Markup.cancel_invoice
    )

    amount = int(message.text)
    invoice_id = await message.bot.database.create_invoice(amount)

    invoice_message = await message.answer_invoice(
        title="شحن الرصيد",
        description="بعد الشحن سيبدأ البوت العمل في الخلفية تلقائيًا",
        payload=str(invoice_id),
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label="شحن الرصيد",
                amount=amount
            )
        ]
    )
    await message.bot.database.additional_message_id_invoice(
        invoice_id, invoice_message.message_id
    )
    await state.set_data({
        "invoice_id": invoice_id
    })
    await state.set_state(PaymentsStates.wait_payment)


@router.pre_checkout_query(StateFilter(PaymentsStates.wait_payment))
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    is_pending = await pre_checkout_query.bot.database.is_invoice_pending(
        int(pre_checkout_query.invoice_payload)
    )

    if is_pending:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(
            ok=False,
            error_message="❌ هذه الفاتورة لم تعد صالحة أو تم رفضها."
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
        text="✅ تم الدفع بنجاح", 
        reply_markup=Markup.start
    )
    await message.answer(
        text="💰 تم شحن رصيدك بنجاح!",
        reply_markup=Markup.configurator([Markup.back('profile')])
    )

    await state.clear()


@router.callback_query(F.data == 'buy_vip')
async def vip_info_handler(call: CallbackQuery):
    await call.message.edit_text(
        text=f"💎 سعر الاشتراك VIP هو {call.bot.config.vip_price} عملة.",
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
            text="⚠️ أنت بالفعل مشترك في VIP.", show_alert=True
        )

    if user_db.balance < call.bot.config.vip_price:
        return await call.answer(
            text="⚠️ رصيدك غير كافٍ لشراء VIP.",
            show_alert=True
        )

    await call.bot.database.update_balance(
        call.from_user.id, 
        call.bot.config.vip_price,
        operation=BalanceOperation.SUBTRACT
    )
    await call.bot.database.grant_vip(call.from_user.id, True)

    await call.message.edit_text(
        text="🎉 تم شراء اشتراك VIP بنجاح!",
        reply_markup=Markup.configurator(
            [Markup.back('profile')]
        )
    )