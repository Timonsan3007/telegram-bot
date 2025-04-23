# __init__.py

# Объявляем структуру импорта для удобного использования пакета
from currencies import send_currency_rates
from holidays import get_holiday_info
from reminders import get_todays_reminders
from weather import get_weather_forecast
from transport import get_transport_schedule
from quotes import get_random_quote

__all__ = [
    "get_all_rates",
    "get_holiday_info",
    "get_todays_reminders",
    "get_weather_forecast",
    "get_transport_schedule",
    "get_random_quote",
]
