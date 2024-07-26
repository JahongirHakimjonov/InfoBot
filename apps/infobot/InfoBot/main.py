import logging
import os

import django
from aiogram.utils import executor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.infobot.InfoBot.handlers import dp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
