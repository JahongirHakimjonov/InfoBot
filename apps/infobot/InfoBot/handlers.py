import os

from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        KeyboardButton("O'zbek🇺🇿"),
        KeyboardButton("Русский🇷🇺"),
    )
    await message.reply(_("Iltimos, tilni tanlang:"), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["O'zbek🇺🇿", "Русский🇷🇺"])
async def process_language_selection(message: types.Message):
    lang_code = None
    if message.text == "O'zbek🇺🇿":
        lang_code = "uz"
    elif message.text == "Русский🇷🇺":
        lang_code = "ru"

    if lang_code:
        user = await sync_to_async(BotUser.objects.get)(
            telegram_id=message.from_user.id
        )
        user.language_code = lang_code
        await sync_to_async(user.save)()

        activate(lang_code)

        if lang_code == "uz":
            alert = "🇺🇿"
        elif lang_code == "ru":
            alert = "🇷🇺"
        # elif lang_code == "en":
        #     alert = "🇬🇧"

        await message.answer(_("Til tanlandi!") + f" {alert}")

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        keyboard.add(
            KeyboardButton(str(_("Boshlash"))),
            KeyboardButton(str(_("Kompaniya haqida ma'lumot"))),
            KeyboardButton(str(_("Xizmatlar"))),
            KeyboardButton(str(_("Yangiliklar"))),
            KeyboardButton(str(_("Kontaktlar"))),
            KeyboardButton(str(_("FAQ"))),
            KeyboardButton(str(_("Hamkorlar"))),
            KeyboardButton(str(_("Investorlar"))),
        )
        await message.answer(str(_("Xush kelibsiz! Tanlovni bajaring:")), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == str(_("Boshlash")))
async def process_start(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton(str(_("Kompaniya haqida ma'lumot"))),
        KeyboardButton(str(_("Xizmatlar"))),
        KeyboardButton(str(_("Yangiliklar"))),
        KeyboardButton(str(_("Kontaktlar"))),
        KeyboardButton(str(_("FAQ"))),
        KeyboardButton(str(_("Hamkorlar"))),
        KeyboardButton(str(_("Investorlar")))
    )
    await message.answer(str(_("Xush kelibsiz! Tanlovni bajaring:")), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == _("Kompaniya haqida ma'lumot"))
async def process_company_info(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

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

    await message.answer(message_text)


@dp.message_handler(lambda message: message.text == _("Hamkorlar"))
async def process_partners(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(str(_("Hamkorlarni ko'rish"))))
    keyboard.add(KeyboardButton(str(_("Hamkorlik uchun ariza berish"))))
    keyboard.add(KeyboardButton(str(_("Orqaga"))))
    await message.answer(str(_("Hamkorlar:")), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == _("Hamkorlarni ko'rish"))
async def process_view_partners(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    partner_list = await sync_to_async(list)(Partner.objects.all())

    message_text = _("Hamkorlar:\n\n")
    for partner in partner_list:
        message_text += f"{partner.name}\n\n{partner.description}\n"
        if partner.logo and partner.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(partner.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo,
                        caption=f"{partner.name}\n\n{partner.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += _("Logo URL noto'g'ri.\n")
        else:
            message_text += "\n"

            await message.answer(message_text)


@dp.message_handler(lambda message: message.text == str(_("Investorlar")))
async def process_investors(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(str(_("Investorlarni ko'rish"))))
    keyboard.add(KeyboardButton(str(_("Investitsiya uchun ariza berish"))))
    keyboard.add(KeyboardButton(str(_("Orqaga"))))
    await message.answer(str(_("Investorlar:")), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == _("Investorlarni ko'rish"))
async def process_view_investors(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    investor_list = await sync_to_async(list)(Investor.objects.all())

    message_text = _("Investorlar:\n\n")
    for investor in investor_list:
        message_text += f"{investor.name}\n\n{investor.description}\n"
        if investor.logo and investor.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(investor.logo)}"
            print(f"Photo Path: {photo_path}")
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo,
                        caption=f"{investor.name}\n\n{investor.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += _("Logo URL noto'g'ri.\n")
        else:
            message_text += "\n"
            await message.answer(message_text)


@dp.message_handler(lambda message: message.text == _("Xizmatlar"))
async def process_services(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    service_list = await sync_to_async(list)(Service.objects.all())

    for service in service_list:
        message_text = f"{service.name}\n{service.description}\n\n"
        if service.logo and service.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(service.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await message.answer(_("Logo URL noto'g'ri.\n"))
        else:
            await message.answer(message_text)


@dp.message_handler(lambda message: message.text == _("Yangiliklar"))
async def process_news(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    news_list = await sync_to_async(list)(News.objects.all())

    for news in news_list:
        message_text = f"{news.title}\n{news.description}\n\n"
        if news.image and news.image.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.image)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await message.answer(_("Rasm URL noto'g'ri.\n"))
        else:
            await message.answer(message_text)


@dp.message_handler(lambda message: message.text == _("Kontaktlar"))
async def process_contacts(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    contacts_list = await sync_to_async(list)(Contact.objects.all())

    message_text = _("Kontaktlar:\n\n")
    for contact in contacts_list:
        message_text += (
            f"Ism: {contact.name}\nTelefon: {contact.phone}\nEmail: {contact.email}\n\n"
        )

    await message.answer(message_text)


@dp.message_handler(lambda message: message.text == _("FAQ"))
async def process_faq(message: types.Message):
    user = await sync_to_async(BotUser.objects.get)(telegram_id=message.from_user.id)
    activate(user.language_code)

    faq_list = await sync_to_async(list)(FAQ.objects.all())

    message_text = _("FAQ:\n\n")
    for faq in faq_list:
        message_text += f"Savol: {faq.question}\nJavob: {faq.answer}\n\n"

    await message.answer(message_text)
