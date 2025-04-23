import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import CURRENCY_API_KEY, CURRENCY_URL, BITCOIN_API_URL

# Добавляем родительскую директорию в путь поиска модулей (если вызывается из другого места)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Смайлики для валют
CURRENCY_ICONS = {
    "USD": "💵",
    "EUR": "💶",
    "CNY": "🇨🇳",
    "BTC": "₿",
    "RUB": "🇷🇺"
}

# Смайлики для динамики изменения
CHANGE_ICONS = {
    "up": "🟢",     # Рост
    "down": "🔴",   # Снижение
    "neutral": "➡️" # Без изменений
}

# Форматирование чисел с пробелами для тысяч
def format_number(value):
    """
    Форматирует число с пробелами для тысяч и запятой для дробной части.
    """
    return "{:,.2f}".format(value).replace(",", " ").replace(".", ",")

# Форматирование изменений валют
def format_currency_change(change):
    """
    Форматирует изменение курса валюты с добавлением знака + для роста.
    """
    sign = "+" if change > 0 else ""
    return f"{sign}{format_number(change)}"

def get_bitcoin_rate():
    """
    Получение курса биткойна с динамикой изменений.
    """
    try:
        # Текущий курс биткойна
        current_url = f"{BITCOIN_API_URL}?ids=bitcoin&vs_currencies=usd"
        current_response = requests.get(current_url, timeout=10)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Исторический курс биткойна (вчерашний день)
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
        historical_url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={yesterday}&localization=false"
        historical_response = requests.get(historical_url, timeout=10)
        historical_response.raise_for_status()
        historical_data = historical_response.json()

        # Текущий курс доллара к рублю
        currency_url = f"{CURRENCY_URL}latest.json?app_id={CURRENCY_API_KEY}"
        currency_response = requests.get(currency_url, timeout=10)
        currency_response.raise_for_status()
        currency_data = currency_response.json()

        if (
            "bitcoin" not in current_data
            or "market_data" not in historical_data
            or "rates" not in currency_data
        ):
            return "❗ Ошибка: данные о биткойне или курсе валют недоступны."

        # Получение данных
        btc_usd = current_data["bitcoin"]["usd"]
        btc_usd_yesterday = historical_data["market_data"]["current_price"]["usd"]
        usd_to_rub = currency_data["rates"]["RUB"]

        # Рассчитываем курс биткойна в рублях (BTC/USD * USD/RUB)
        btc_rub = btc_usd * usd_to_rub
        btc_rub_yesterday = btc_usd_yesterday * usd_to_rub  # Используем тот же курс доллара

        # Вычисление изменений
        usd_change = btc_usd - btc_usd_yesterday
        rub_change = usd_change * usd_to_rub  # Пересчет изменения в рублях

        # Определение знаков и значков изменений
        usd_sign = "🟢" if usd_change > 0 else "🔴" if usd_change < 0 else "➡️"
        rub_sign = "🟢" if rub_change > 0 else "🔴" if rub_change < 0 else "➡️"

        # Форматирование
        btc_usd_formatted = format_number(btc_usd)
        btc_rub_formatted = format_number(btc_rub)
        usd_change_formatted = format_currency_change(usd_change)
        rub_change_formatted = format_currency_change(rub_change)

        # Возвращаем отформатированный вывод
        return (
            f"BTC ₿: {btc_usd_formatted} $ ({usd_sign} {usd_change_formatted} $)\n"
            f"      {btc_rub_formatted} ₽ ({rub_sign} {rub_change_formatted} ₽)"
        )
    except Exception as e:
        return f"Ошибка при запросе данных о биткойне: {e}"



# Получение курсов валют с динамикой изменений
def get_currency_rates():
    """
    Получение курсов валют и динамики изменений.
    """
    try:
        latest_url = f"{CURRENCY_URL}latest.json?app_id={CURRENCY_API_KEY}"
        latest_response = requests.get(latest_url, timeout=10)
        latest_response.raise_for_status()
        latest_data = latest_response.json()

        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        historical_url = f"{CURRENCY_URL}/historical/{yesterday}.json?app_id={CURRENCY_API_KEY}"
        historical_response = requests.get(historical_url, timeout=10)
        historical_response.raise_for_status()
        historical_data = historical_response.json()

        if "rates" not in latest_data or "rates" not in historical_data:
            return "Ошибка получения данных курсов."

        latest_rub_rate = latest_data["rates"]["RUB"]
        historical_rub_rate = historical_data["rates"]["RUB"]

        target_currencies = ["USD", "EUR", "CNY"]
        results = ["*Курс валют:*"]

        for currency in target_currencies:
            latest_rate_to_usd = latest_data["rates"].get(currency)
            historical_rate_to_usd = historical_data["rates"].get(currency)
            if latest_rate_to_usd and historical_rate_to_usd:
                latest_rate_to_rub = latest_rub_rate / latest_rate_to_usd
                historical_rate_to_rub = historical_rub_rate / historical_rate_to_usd
                change = latest_rate_to_rub - historical_rate_to_rub

                # Исправление ошибки округления
                if abs(change) < 0.005:  # Если изменение слишком мало, считаем его нулевым
                    change = 0

                change_formatted = format_currency_change(change)
                change_emoji = CHANGE_ICONS["up" if change > 0 else "down" if change < 0 else "neutral"]

                results.append(
                    f"{currency} {CURRENCY_ICONS.get(currency, '')}: {format_number(latest_rate_to_rub)} ₽ ({change_emoji} {change_formatted} ₽)"
                )
            else:
                results.append(f"{currency}: данные недоступны.")

        # Добавление курса биткойна
        results.append(get_bitcoin_rate())

        return "\n".join(results)

    except requests.RequestException as e:
        return f"Ошибка соединения: {e}"
    except Exception as e:
        return f"Непредвиденная ошибка: {e}"

# Получение ключевой ставки ЦБ РФ
def get_key_rate():
    url = "https://www.cbr.ru/eng/hd_base/KeyRate/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'class': 'data'})
        if table:
            rows = table.find_all('tr')
            latest_row = rows[1]
            rate_cell = latest_row.find_all('td')[1].text.strip()
            return float(rate_cell.replace(",", "."))
        return "Не удалось найти ключевую ставку."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе данных: {e}"
    except Exception as e:
        return f"Не удалось обработать ответ: {e}"

# Общая функция для получения всех данных
def get_all_financial_data():
    currency_data = get_currency_rates()
    key_rate = get_key_rate()

    if isinstance(key_rate, float):
        key_rate_str = f"*Ключевая ставка ЦБ РФ:* {format_number(key_rate)}%"
    else:
        key_rate_str = key_rate

    return f"{currency_data}\n\n{key_rate_str}"

# Пример вызова функции для тестирования
if __name__ == "__main__":
    print(get_all_financial_data())
