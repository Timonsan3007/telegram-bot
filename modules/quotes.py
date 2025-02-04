import requests

def get_quote_of_the_day():
    """
    Получает цитату дня из API Forismatic и оформляет её.
    """
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Извлекаем текст цитаты и автора
        quote = data.get('quoteText', 'Цитата недоступна.')
        author = data.get('quoteAuthor', 'Неизвестный автор')

        # Возвращаем оформленную цитату
        return f"✨ *Цитата дня:*\n❗ {quote} — {author}"
    except requests.RequestException as e:
        return f"Ошибка при запросе цитаты: {e}"

# Пример вызова функции
if __name__ == "__main__":
    print(get_quote_of_the_day())