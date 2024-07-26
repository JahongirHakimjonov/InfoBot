from aiogram.utils import executor
from django.core.management.base import BaseCommand

from apps.infobot.InfoBot.handlers import dp


class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
