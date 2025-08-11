from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.data import Text, Markup
from src.utils import DefaultUtils, BalanceOperation

rname = 'admin'
router = Router()


def is_owner_filter(message: Message):
    return message.from_user.id == message.bot.config.owner


@router.message(Command('give_vip'), is_owner_filter)
async def give_vip_handler(message: Message):
    try:
        user_id = int(message.text.split()[1])
        user = await message.bot.database.get_user(user_id)

        if not user:
            return await message.answer("❌ المستخدم غير موجود")

        await message.bot.database.grant_vip(user_id, True)
        await message.answer(f"✅ تم منح حالة VIP للمستخدم {user_id}")
    except (IndexError, ValueError):
        await message.answer("❌ الاستخدام: /give_vip <معرف_المستخدم>")


@router.message(Command('remove_vip'), is_owner_filter)
async def remove_vip_handler(message: Message):
    try:
        user_id = int(message.text.split()[1])
        user = await message.bot.database.get_user(user_id)

        if not user:
            return await message.answer("❌ المستخدم غير موجود")

        await message.bot.database.grant_vip(user_id, False)
        await message.answer(f"✅ تم إزالة حالة VIP من المستخدم {user_id}")
    except (IndexError, ValueError):
        await message.answer("❌ الاستخدام: /remove_vip <معرف_المستخدم>")


@router.message(Command('give_stars'), is_owner_filter)
async def give_stars_handler(message: Message):
    try:
        args = message.text.split()
        user_id = int(args[1])
        amount = int(args[2])

        user = await message.bot.database.get_user(user_id)
        if not user:
            return await message.answer("❌ المستخدم غير موجود")

        await message.bot.database.update_balance(user_id, amount, BalanceOperation.ADD)
        await message.answer(f"✅ تم منح {amount} نجمة للمستخدم {user_id}")
    except (IndexError, ValueError):
        await message.answer("❌ الاستخدام: /give_stars <معرف_المستخدم> <العدد>")


@router.message(Command('remove_stars'), is_owner_filter)
async def remove_stars_handler(message: Message):
    try:
        args = message.text.split()
        user_id = int(args[1])
        amount = int(args[2])

        user = await message.bot.database.get_user(user_id)
        if not user:
            return await message.answer("❌ المستخدم غير موجود")

        if user.balance < amount:
            return await message.answer("❌ المستخدم لا يملك عدد كافٍ من النجوم")

        await message.bot.database.update_balance(user_id, amount, BalanceOperation.SUBTRACT)
        await message.answer(f"✅ تم إزالة {amount} نجمة من المستخدم {user_id}")
    except (IndexError, ValueError):
        await message.answer("❌ الاستخدام: /remove_stars <معرف_المستخدم> <العدد>")