import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import WEATHER_API_KEY, WEATHER_URL

# Добавление текущего пути для корректного импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Смайлики для погодных условий
WEATHER_ICONS = {
    "ясно": "🌞",
    "облачно": "☁️",
    "пасмурно": "🌥️",
    "переменная облачность": "⛅",
    "облачно с прояснениями": "🌤️",
    "небольшая облачность": "🌤",
    "дождь": "🌧️",
    "снег": "🌨️",
    "гроза": "🌩️",
    "туман": "🌫️",
}

# Смайлики для температуры
def get_temp_icon(temp):
    return "❄️" if temp < 0 else "☀️"

# Смайлики для силы ветра
def get_wind_speed_icon(speed):
    if speed < 1:
        return "🍃"
    elif speed < 5:
        return "🌬️"
    elif speed < 10:
        return "💨"
    else:
        return "🌪️"

# Функция для перевода направления ветра в сокращенный формат
def wind_direction_short(deg):
    if 22.5 <= deg < 67.5:
        return "в. с-в ↗️"  # Северо-восточный ветер дует на юго-запад
    elif 67.5 <= deg < 112.5:
        return "в. в ➡️"  # Восточный ветер дует на запад
    elif 112.5 <= deg < 157.5:
        return "в. ю-в ↘️"  # Юго-восточный ветер дует на северо-запад
    elif 157.5 <= deg < 202.5:
        return "в. ю ⬇️"  # Южный ветер дует на север
    elif 202.5 <= deg < 247.5:
        return "в. ю-з ↙️"  # Юго-западный ветер дует на северо-восток
    elif 247.5 <= deg < 292.5:
        return "в. з ⬅️"  # Западный ветер дует на восток
    elif 292.5 <= deg < 337.5:
        return "в. с-з ↖️"  # Северо-западный ветер дует на юго-восток
    else:
        return "в. с ⬆️"  # Северный ветер дует на юг

    idx = int((degree + 22.5) // 45) % 8
    return directions[full_directions[idx]]

# Функция для получения прогноза погоды
def get_weather_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q=Volgograd&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url, timeout=10).json()
        forecast_list = response.get('list', [])
        if not forecast_list:
            return "🌤️ Не удалось получить данные о погоде."

        weather_info = ["*Погода в Волгограде:*"]
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        today_date = f"📅 *{today.strftime('%d.%m.%Y')}*"
        tomorrow_date = f"📅 *{tomorrow.strftime('%d.%m.%Y')}*"

        today_weather = []
        tomorrow_weather = []

        for forecast in forecast_list:
            forecast_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            time = forecast_time.strftime("%H:%M")
            temp = round(forecast['main']['temp'])  # Округляем температуру
            desc = forecast['weather'][0]['description']
            wind_speed = round(forecast['wind']['speed'])  # Округляем скорость ветра
            wind_deg = forecast['wind']['deg']
            wind_dir = wind_direction_short(wind_deg)
            rain = forecast.get('rain', {}).get('1h', 0)
            snow = forecast.get('snow', {}).get('1h', 0)

            # Логика формирования описания осадков
            if rain > 0:
                precip = f"дождь: {rain:.1f} мм за час"
            elif snow > 0:
                precip = f"снег: {snow:.1f} мм за час"
            else:
                precip = "б/о"

            # Обработка описания погоды и выбор иконки
            main_condition = desc.split()[0]  # Берем первое слово из описания для общего состояния
            icon = WEATHER_ICONS.get(main_condition, '🌤')  # Ищем иконку по общему состоянию

            # Формирование строки для текущего прогноза
            weather_line = (
                f"{time} {icon} {main_condition.capitalize()[:3]}., "  # Сокращение состояния
                f"t: {temp}°C {get_temp_icon(temp)}, "
                f"{wind_dir}: {wind_speed} м/с 🌬️"
            )

            if forecast_time.date() == today.date():
                today_weather.append(weather_line)
            elif forecast_time.date() == tomorrow.date():
                tomorrow_weather.append(weather_line)

        # Убираем лишние пустые строки, добавляем ровно одну между блоками
        if today_weather:
            weather_info.append(f"{today_date}:\n" + "\n".join(today_weather))
        if tomorrow_weather:
            weather_info.append(f"\n{tomorrow_date}:\n" + "\n".join(tomorrow_weather))

        return "\n".join(weather_info)
    except requests.exceptions.RequestException as e:
        return f"❗ Ошибка при запросе данных: {e}"

# Функция для получения информации о восходе и заходе солнца
def get_sun_info(latitude, longitude):
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            return "Не удалось получить данные о солнце."

        # Извлекаем данные
        sunrise_utc = datetime.fromisoformat(data["results"]["sunrise"])
        sunset_utc = datetime.fromisoformat(data["results"]["sunset"])
        day_length = data["results"]["day_length"]

        # Перевод времени в локальную зону (UTC+3 для Волгограда)
        local_offset = timedelta(hours=3)
        sunrise_local = (sunrise_utc + local_offset).strftime("%H:%M")
        sunset_local = (sunset_utc + local_offset).strftime("%H:%M")
        day_length_str = str(timedelta(seconds=int(day_length)))

        return (
            f"*Восход и заход солнца:*\n"
            f"🌅 Восход: {sunrise_local}\n"
            f"🌇 Закат: {sunset_local}\n"
            f"⏳ Долгота дня: {day_length_str}"
        )
    except requests.RequestException as e:
        return f"Ошибка соединения: {e}"
    except Exception as e:
        return f"Не удалось обработать данные: {e}"

# Функция для получения температуры Волги
def get_volga_temperature():
    url = "https://seatemperature.ru/current/russia/volga-volgograd-sea-temperature"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        temp_block = soup.find("div", id="temp1")
        if temp_block:
            temperature = temp_block.find("h3").text.strip()
            return f"🌊 Температура воды в Волге: {temperature}"
        else:
            return "Не удалось найти информацию о температуре воды."
    except requests.RequestException as e:
        return f"Ошибка при получении данных о температуре воды: {e}"


# Итоговая функция, объединяющая данные о погоде, солнце и температуре Волги
def get_weather_and_sun_info():
    weather = get_weather_forecast()
    sun_info = get_sun_info(latitude=48.7081, longitude=44.5133)  # Координаты Волгограда
    volga_temp = get_volga_temperature()

    # Убираем лишние пустые строки, добавляем ровно одну между блоками
    return f"{weather}\n\n{sun_info}\n\n{volga_temp}"

# Пример вызова функций
if __name__ == "__main__":
    print(get_weather_and_sun_info())
