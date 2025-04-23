import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN, CHAT_ID
from modules.holidays import get_holiday_info
from modules.currencies import get_all_financial_data
from modules.weather import get_weather_and_sun_info
from modules.transport import get_transport_schedule
from modules.quotes import get_quote_of_the_day
from modules.scheduler import start_scheduler
from modules.reminders import get_todays_reminders

async def build_summary_message():
    """
    Формирование общего сообщения для отправки.
    """
    parts = []

    # Получаем данные
    weather_and_sun_info = get_weather_and_sun_info()  # Данные о погоде и солнце
    currency = get_all_financial_data()  # Финансовая информация
    holiday_info = get_holiday_info()  # Праздники
    reminders = get_todays_reminders()  # Напоминания
    transport_schedule = get_transport_schedule()  # Расписание транспорта
    daily_quote = get_quote_of_the_day()  # Цитата дня

    # Формируем итоговое сообщение
    parts.extend([
        weather_and_sun_info,
        currency,
        holiday_info,
        reminders,
        transport_schedule,
        daily_quote,
    ])

    return "\n\n".join(filter(None, parts))

async def send_daily_summary(application):
    """
    Отправка общего сообщения в чат.
    """
    message = await build_summary_message()
    print(f"Отправка сообщения: {message[:50]}...")  # Отладочное сообщение
    if message:
        await application.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start_command(update, context):
    """
    Обработчик команды /start.
    """
    message = await build_summary_message()
    await update.message.reply_text(message, parse_mode="Markdown")

async def main():
    """
    Основная функция для запуска бота.
    """
    # Создание приложения Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler("start", start_command))

    # Запуск планировщика
    start_scheduler(application, send_daily_summary)

    print("Бот запущен. Нажмите Ctrl+C для остановки.")

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
