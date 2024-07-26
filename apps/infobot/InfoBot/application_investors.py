from aiogram import types
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from django.utils.translation import activate, gettext_lazy as _

from apps.infobot.InfoBot.handlers import dp, bot
from apps.infobot.InfoBot.states import InvestmentForm
from apps.infobot.models import ApplicationInvestor, BotUser


@dp.callback_query_handler(lambda message: message.text == _("Investitsiya uchun ariza berish"))
async def process_apply_investment(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, _("Iltimos, to'liq ismingizni yuboring:"))
    await InvestmentForm.full_name.set()


@dp.message_handler(state=InvestmentForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply(_("Iltimos, telefon raqamingizni yuboring:"))
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply(_("Iltimos, manzilingizni yuboring:"))
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.address)
async def process_address(message: types.Message, state: FSMContext):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply(_("Iltimos, xabaringizni yuboring:"))
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.user_message)
async def process_message(message: types.Message, state: FSMContext):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    async with state.proxy() as data:
        user_message = message.text
        await sync_to_async(ApplicationInvestor.objects.create)(
            full_name=data["full_name"],
            phone=data["phone"],
            address=data["address"],
            message=user_message,
        )
    await message.reply(_("Arizangiz qabul qilindi!"))
    await state.finish()
