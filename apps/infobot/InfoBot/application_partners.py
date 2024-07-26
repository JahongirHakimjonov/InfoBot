from aiogram import types
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from apps.infobot.InfoBot.handlers import bot, dp
from apps.infobot.InfoBot.states import PartnershipForm
from apps.infobot.models import ApplicationPartner


@dp.callback_query_handler(lambda c: c.data == "apply_partnership")
async def process_apply_partnership(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Please send your full name:")
    await PartnershipForm.full_name.set()


@dp.message_handler(state=PartnershipForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply("Please send your phone number:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply("Please send your address:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply("Please send your message:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.user_message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_message = message.text
        await sync_to_async(ApplicationPartner.objects.create)(
            full_name=data["full_name"],
            phone=data["phone"],
            address=data["address"],
            message=user_message,
        )
    await message.reply("Your application has been submitted!")
    await state.finish()
