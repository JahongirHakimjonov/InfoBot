import os

from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest
from asgiref.sync import sync_to_async
from django.utils.translation import activate, gettext as _

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

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("O'zbek🇺🇿", callback_data="lang_uz"),
        InlineKeyboardButton("Русский🇷🇺", callback_data="lang_ru"),
        InlineKeyboardButton("English🇬🇧", callback_data="lang_en"),
    )
    await message.reply("Please select your language:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith("lang_"))
async def process_language_selection(callback_query: types.CallbackQuery):
    lang_code = callback_query.data.split("_")[1]
    user = await sync_to_async(BotUser.objects.get)(
        telegram_id=callback_query.from_user.id
    )
    user.language_code = lang_code
    await sync_to_async(user.save)()

    activate(lang_code)
    # await bot.delete_message(
    #     callback_query.from_user.id, callback_query.message.message_id
    # )
    if lang_code == "uz":
        alert = "🇺🇿"
    elif lang_code == "ru":
        alert = "🇷🇺"
    elif lang_code == "en":
        alert = "🇬🇧"
        return alert
    await bot.answer_callback_query(
        callback_query.id, _(f"Language selected! {alert}"), show_alert=True
    )

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(str(_("Company Info")), callback_data="company_info")
    )
    keyboard.add(InlineKeyboardButton(str(_("Services")), callback_data="services"))
    keyboard.add(InlineKeyboardButton(str(_("News")), callback_data="news"))
    keyboard.add(InlineKeyboardButton(str(_("Contacts")), callback_data="contacts"))
    keyboard.add(InlineKeyboardButton(str(_("FAQ")), callback_data="faq"))
    keyboard.add(InlineKeyboardButton(str(_("Partners")), callback_data="partners"))
    keyboard.add(InlineKeyboardButton(str(_("Investors")), callback_data="investors"))
    keyboard.add(InlineKeyboardButton(str(_("Inline")), callback_data="inline"))
    await bot.send_message(
        callback_query.from_user.id,
        str(_("Welcome! Choose an option:")),
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data == "start")
async def process_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Company Info", callback_data="company_info"))
    keyboard.add(InlineKeyboardButton("Services", callback_data="services"))
    keyboard.add(InlineKeyboardButton("News", callback_data="news"))
    keyboard.add(InlineKeyboardButton("Contacts", callback_data="contacts"))
    keyboard.add(InlineKeyboardButton("FAQ", callback_data="faq"))
    keyboard.add(InlineKeyboardButton("Partners", callback_data="partners"))
    keyboard.add(InlineKeyboardButton("Investors", callback_data="investors"))
    await bot.send_message(
        callback_query.from_user.id,
        _("Welcome! Choose an option:"),
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = "Company Info:\n\n"
    for info in company_info_list:
        message_text += f"Name: {info.name}\nDescription: {info.description}\n\nPhone: {info.phone}\nEmail: {info.email}\nWebsite: {info.website}\n\n"

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "partners")
async def process_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("View partnesr", callback_data="view_partners"))
    keyboard.add(
        InlineKeyboardButton("Apply for Partnership", callback_data="apply_partnership")
    )
    keyboard.add(InlineKeyboardButton("Back", callback_data="start"))
    await bot.send_message(
        callback_query.from_user.id, "Partnesr:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "view_partners")
async def process_view_partners(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    partner_list = await sync_to_async(list)(Partner.objects.all())

    message_text = "Partners:\n\n"
    for partner in partner_list:
        message_text += f"Name: {partner.name}\nDescription: {partner.description}\n"
        if partner.logo and partner.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(partner.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"Name: {partner.name}\nDescription: {partner.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"

            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "investors")
async def process_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("View Investors", callback_data="view_investors"))
    keyboard.add(
        InlineKeyboardButton("Apply for Investment", callback_data="apply_investment")
    )
    keyboard.add(InlineKeyboardButton("Back", callback_data="start"))
    await bot.send_message(
        callback_query.from_user.id, "Investors:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "view_investors")
async def process_view_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    investor_list = await sync_to_async(list)(Investor.objects.all())

    message_text = "Investors:\n\n"
    for investor in investor_list:
        message_text += f"Name: {investor.name}\nDescription: {investor.description}\n"
        if investor.logo and investor.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(investor.logo)}"
            print(f"Photo Path: {photo_path}")
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"Name: {investor.name}\nDescription: {investor.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = "Company Info:\n\n"
    for info in company_info_list:
        message_text += (
            f"Name: {info.name}\n"
            f"Description: {info.description}\n\n"
            f"Phone: {info.phone}\nEmail: {info.email}\n"
            f"Website: {info.website}\n\n"
        )

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "services")
async def process_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    news_list = await sync_to_async(list)(Service.objects.all())

    for news in news_list:
        message_text = f"Title: {news.name}\nDescription: {news.description}\n\n"
        if news.logo and news.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await bot.delete_message(
                        callback_query.from_user.id, callback_query.message.message_id
                    )
                    await bot.send_message(
                        callback_query.from_user.id, "Image URL is invalid.\n"
                    )
        else:
            await bot.delete_message(
                callback_query.from_user.id, callback_query.message.message_id
            )
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "news")
async def process_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    news_list = await sync_to_async(list)(News.objects.all())

    for news in news_list:
        message_text = f"Title: {news.title}\nDescription: {news.description}\n\n"
        if news.image and news.image.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.image)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await bot.delete_message(
                        callback_query.from_user.id, callback_query.message.message_id
                    )
                    await bot.send_message(
                        callback_query.from_user.id, "Image URL is invalid.\n"
                    )
        else:
            await bot.delete_message(
                callback_query.from_user.id, callback_query.message.message_id
            )
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "contacts")
async def process_contacts(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    contacts_list = await sync_to_async(list)(Contact.objects.all())

    message_text = "Contacts:\n\n"
    for contact in contacts_list:
        message_text += (
            f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}\n\n"
        )

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "faq")
async def process_faq(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    faq_list = await sync_to_async(list)(FAQ.objects.all())

    message_text = "FAQ:\n\n"
    for faq in faq_list:
        message_text += f"Question: {faq.question}\nAnswer: {faq.answer}\n\n"

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(callback_query.from_user.id, message_text)
