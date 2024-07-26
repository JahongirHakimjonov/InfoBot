import os

from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest
from asgiref.sync import sync_to_async
from django.utils.translation import activate, gettext_lazy as _

from apps.infobot.models import (
    BotUser,
    CompanyInfo,
    Partner,
    Investor,
    Service,
    News,
    Contact,
    FAQ,
)
from core import settings

storage = MemoryStorage()
API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start", "lang"])
async def send_welcome(message: types.Message):
    user, created = await sync_to_async(BotUser.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        },
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("O'zbek🇺🇿", callback_data="lang_uz"),
        InlineKeyboardButton("Русский🇷🇺", callback_data="lang_ru"),
    )
    await message.reply(_("Iltimos, tilni tanlang:"), reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ["lang_uz", "lang_ru"])
async def process_language_selection(callback_query: types.CallbackQuery):
    lang_code = None
    if callback_query.data == "lang_uz":
        lang_code = "uz"
    elif callback_query.data == "lang_ru":
        lang_code = "ru"

    if lang_code:
        user = await sync_to_async(BotUser.objects.get)(
            telegram_id=callback_query.from_user.id
        )
        user.language_code = lang_code
        await sync_to_async(user.save)()

        activate(lang_code)

        if lang_code == "uz":
            alert = "🇺🇿"
        elif lang_code == "ru":
            alert = "🇷🇺"
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, _("Til tanlandi!") + f" {alert}")

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton(str(_("Kompaniya haqida ma'lumot")), callback_data="company_info"),
            InlineKeyboardButton(str(_("Xizmatlar")), callback_data="services"),
            InlineKeyboardButton(str(_("Yangiliklar")), callback_data="news"),
            InlineKeyboardButton(str(_("Kontaktlar")), callback_data="contacts"),
            InlineKeyboardButton(str(_("FAQ")), callback_data="faq"),
            InlineKeyboardButton(str(_("Hamkorlar")), callback_data="partners"),
            InlineKeyboardButton(str(_("Investorlar")), callback_data="investors"),
        )
        await bot.send_message(callback_query.from_user.id, str(_("Xush kelibsiz! Tanlovni bajaring:")),
                               reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "start")
async def process_start(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(str(_("Kompaniya haqida ma'lumot")), callback_data="company_info"),
        InlineKeyboardButton(str(_("Xizmatlar")), callback_data="services"),
        InlineKeyboardButton(str(_("Yangiliklar")), callback_data="news"),
        InlineKeyboardButton(str(_("Kontaktlar")), callback_data="contacts"),
        InlineKeyboardButton(str(_("FAQ")), callback_data="faq"),
        InlineKeyboardButton(str(_("Hamkorlar")), callback_data="partners"),
        InlineKeyboardButton(str(_("Investorlar")), callback_data="investors")
    )
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, str(_("Xush kelibsiz! Tanlovni bajaring:")),
                           reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = _("Kompaniya haqida ma'lumot:\n\n")
    for info in company_info_list:
        message_text += (
            f"{info.name}\n"
            f"{info.description}\n\n"
            f"{info.phone}\n"
            f"{info.email}\n"
            f"{info.website}\n\n"
        )
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "partners")
async def process_partners(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Hamkorlarni ko'rish")), callback_data="view_partners"))
    keyboard.add(InlineKeyboardButton(str(_("Hamkorlik uchun ariza berish")), callback_data="apply_partnership"))
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, str(_("Hamkorlar:")), reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "view_partners")
async def process_view_partners(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)

    partner_list = await sync_to_async(list)(Partner.objects.all())

    message_text = _("Hamkorlar:\n\n")
    for partner in partner_list:
        message_text += f"{partner.name}\n\n{partner.description}\n"
        if partner.logo and partner.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(partner.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"{partner.name}\n\n{partner.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += _("Logo URL noto'g'ri.\n")
        else:
            message_text += "\n"
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "investors")
async def process_investors(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Investorlarni ko'rish")), callback_data="view_investors"))
    keyboard.add(InlineKeyboardButton(str(_("Investitsiya uchun ariza berish")), callback_data="apply_investment"))
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, str(_("Investorlar:")), reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "view_investors")
async def process_view_investors(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    investor_list = await sync_to_async(list)(Investor.objects.all())

    message_text = _("Investorlar:\n\n")
    for investor in investor_list:
        message_text += f"{investor.name}\n\n{investor.description}\n"
        if investor.logo and investor.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(investor.logo)}"
            print(f"Photo Path: {photo_path}")
            try:
                with open(photo_path, "rb") as photo:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"{investor.name}\n\n{investor.description}",
                        reply_markup=keyboard,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += _("Logo URL noto'g'ri.\n")
        else:
            message_text += "\n"
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "services")
async def process_services(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    service_list = await sync_to_async(list)(Service.objects.all())

    for service in service_list:
        message_text = f"{service.name}\n{service.description}\n\n"
        if service.logo and service.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(service.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=message_text,
                        reply_markup=keyboard,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.send_message(callback_query.from_user.id, _("Logo URL noto'g'ri.\n"), reply_markup=keyboard)
        else:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "news")
async def process_news(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    news_list = await sync_to_async(list)(News.objects.all())

    for news in news_list:
        message_text = f"{news.title}\n{news.description}\n\n"
        if news.image and news.image.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.image)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=message_text,
                        reply_markup=keyboard,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.send_message(callback_query.from_user.id, _("Rasm URL noto'g'ri.\n"), reply_markup=keyboard)
        else:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "contacts")
async def process_contacts(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    contacts_list = await sync_to_async(list)(Contact.objects.all())

    message_text = _("Kontaktlar:\n\n")
    for contact in contacts_list:
        message_text += (
            f"Ism: {contact.name}\nTelefon: {contact.phone}\nEmail: {contact.email}\n\n"
        )
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "faq")
async def process_faq(callback_query: types.CallbackQuery):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=callback_query.from_user.id)
    activate(user.language_code)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(str(_("Orqaga")), callback_data="start"))
    faq_list = await sync_to_async(list)(FAQ.objects.all())

    message_text = _("FAQ:\n\n")
    for faq in faq_list:
        message_text += f"Savol: {faq.question}\nJavob: {faq.answer}\n\n"
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)
