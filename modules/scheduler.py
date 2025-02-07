import asyncio
import schedule
import time
from datetime import datetime
from config import SCHEDULE_TIMES

def run_task(task, application):
    """
    Обёртка для запуска асинхронной задачи в синхронном планировщике.
    """
    asyncio.run(task(application))

def schedule_jobs(application, send_task):
    """
    Настройка планировщика задач для отправки сообщений в заданное время.
    """
    for time in SCHEDULE_TIMES:
        # Убрали отладочный вывод
        schedule.every().day.at(time).do(run_task, send_task, application)

    # Убрали отладочный вывод
    # print(f"Планировщик настроен на: {', '.join(SCHEDULE_TIMES)}")

def start_scheduler(application, send_task):
    """
    Запуск планировщика в отдельном потоке.
    """
    import threading
    def scheduler_thread():
        schedule_jobs(application, send_task)
        while True:
            # Убрали отладочный вывод
            # print(f"Проверяем задачи в {datetime.now()}")
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=scheduler_thread, daemon=True)
    thread.start()
    # Убрали отладочный вывод
    # print("Планировщик запущен.")
