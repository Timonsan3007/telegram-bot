from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

# Конфигурация бота

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Преобразуем в число

# API-ключи
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
BITCOIN_API_URL = os.getenv("BITCOIN_API_URL")

# Расписание отправки
SCHEDULE_TIMES = eval(os.getenv("SCHEDULE_TIMES"))  # Преобразуем строку в список

# URL API
WEATHER_URL = os.getenv("WEATHER_URL")
CURRENCY_URL = os.getenv("CURRENCY_URL")