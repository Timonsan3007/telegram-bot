from datetime import datetime, timedelta

def format_time_difference(date1, date2):
    """
    Возвращает разницу между двумя датами в формате 'X дней'.
    """
    delta = (date2 - date1).days
    return f"{delta} дней" if delta > 0 else "сегодня"

def get_nearest_date(dates, current_date=None):
    """
    Находит ближайшую дату из списка, начиная с текущей или указанной даты.
    """
    if current_date is None:
        current_date = datetime.now()

    future_dates = [d for d in dates if d >= current_date]
    return min(future_dates, default=None)

def parse_time_string(time_str):
    """
    Преобразует строку времени в объект времени.
    """
    return datetime.strptime(time_str, "%H:%M").time()

def get_next_times(schedule, current_time, limit=3):
    """
    Возвращает список ближайших времен из расписания.
    """
    next_times = []
    for time_str in schedule:
        time_obj = parse_time_string(time_str)
        if time_obj >= current_time:
            next_times.append(time_str)
        if len(next_times) == limit:
            break
    return next_times

def format_currency_change(value):
    """
    Форматирует изменение валюты с добавлением смайликов.
    """
    if value > 0:
        return f"📈 +{value:.2f}"
    elif value < 0:
        return f"📉 {value:.2f}"
    return "➖ 0.00"
