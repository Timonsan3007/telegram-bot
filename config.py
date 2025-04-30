from dotenv import load_dotenv
import os
import json

# Загрузка переменных окружения из .env
load_dotenv()

# Конфигурация бота

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Преобразуем в число

# API-ключи
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
BITCOIN_API_URL = os.getenv("BITCOIN_API_URL")

# Расписание отправки
SCHEDULE_TIMES = json.loads(os.getenv("SCHEDULE_TIMES"))

# URL API
WEATHER_URL = os.getenv("WEATHER_URL")
CURRENCY_URL = os.getenv("CURRENCY_URL")