from datetime import datetime, timedelta

# Список праздников и дней рождения
HOLIDAYS = {
    "01.01": "Новый год 🎉",
    "07.01": "Рождество Христово 🎄",
    "12.01": "День Прокуратуры ⚖️",
    "14.01": "Старый Новый год 🎆",
    "19.01": "Крещение Господне ✝️",
    "22.01": "День рождения Валерии (дочь Карандаша) 🎂",
    "24.01": "День рождения Севостьяновой Леры 🎂",
    "25.01": "Татьянин день (день студента) 🎓",
    "31.01": "Международный день ювелира 💎",
    "02.02": "День сурка 🐿️",
    "08.02": "День российской науки 🔬",
    "13.02": "Всемирный день радио 📻, День рождения брата 🎂, День рождения Сорокина Максима 🎂, День рождения Коржовой Марины 🎂",
    "14.02": "День святого Валентина (день всех влюбленных) ❤️, День компьютерщика 💻",
    "15.02": "Сретение Господне ✝️",
    "23.02": "День защитника Отечества 🛡️, День рождения дяди Валентина Узлова 🎂",
    "26.02": "День рождения Миронова Михаила 🎂",
    "08.03": "Международный женский день 🌹",
    "10.03": "День рождения Дручилова Максима 🎂",
    "16.03": "День рождения тёщи 🎂",
    "27.03": "День МВД 🛡️",
    "28.03": "День рождения Кондрашовой Леры 🎂",
    "30.03": "День рождения Макеева Алексея 🎂",
    "01.04": "День смеха 😂",
    "05.04": "День рождения Сергеева Игоря 🎂",
    "20.04": "Пасха ✝️",
    "22.04": "Международный день Земли 🌍",
    "24.04": "День секретаря 📑",
    "30.04": "День Пожарной охраны 🚒",
    "01.05": "День весны и труда 🌼",
    "07.05": "День радио 📻",
    "09.05": "День Победы 🕊️",
    "11.05": "День рождения Соколова Андрея 🎂",
    "12.05": "День медицинских сестер 💉",
    "13.05": "День Черноморского флота России ⚓",
    "15.05": "Международный день семьи 👨👩👧👦",
    "17.05": "День рождения Папы 🎂",
    "19.05": "День рождения сыночка Саши 🎂",
    "28.05": "День пограничника 🛂",
    "30.05": "День рождения Карандаша 🎂",
    "01.06": "День рождения Артёма Каныгина 🎂, Международный день защиты детей 🧸",
    "08.06": "День социального работника 🤝",
    "12.06": "День России 🇷🇺",
    "15.06": "День медицинского работника 🩺",
    "23.06": "День рождения Дудакова Александра 🎂",
    "27.06": "День молодежи России 🧑🎓",
    "30.06": "День экономиста 📊",
    "03.07": "День ГАИ 🚔",
    "06.07": "День работников морского и речного флота 🚢",
    "11.07": "День рождения Чемериса Сергея 🎂",
    "13.07": "День российской почты 📮, День рыбака 🎣",
    "29.07": "День рождения Паршева Юрия 🎂, День рождения Коваленко Андрея 🎂",
    "02.08": "День Воздушно-десантных войск 🪂",
    "03.08": "День рождения сыночка Кости 🎂, День железнодорожника 🚆",
    "10.08": "День строителя 🏗️",
    "12.08": "День Военно-Воздушных Сил ✈️",
    "13.08": "День физкультурника 🏋️",
    "19.08": "Преображение Господне ✝️",
    "20.08": "День рождения мамы 🎂",
    "22.08": "День Государственного флага Российской Федерации 🇷🇺",
    "26.08": "День шахтера ⛏️",
    "31.08": "День ветеринара 🐾",
    "01.09": "День знаний 📘",
    "02.09": "День окончания Второй мировой войны 🕊️",
    "03.09": "День солидарности в борьбе с терроризмом 🕊️",
    "06.09": "День рождения Нистратова д. Вани 🎂",
    "08.09": "День финансиста 💰, День нашей свадьбы 💍",
    "15.09": "День санитарной службы 🚑",
    "19.09": "День рождения Чекунова Александра 🎂",
    "26.09": "День рождения Верхошапов Виктора 🎂",
    "27.09": "День воспитателя и всех дошкольных работников 🧒, Всемирный день туризма 🗺️",
    "28.09": "День работника атомной промышленности ⚛️",
    "30.09": "День рождения Нистратовой Юлии 🎂, День интернета в России 🌐",
    "01.10": "День Сухопутных войск РФ 🛡️, День пожилого человека 👵",
    "02.10": "День профтехобразования 📚",
    "04.10": "День войск гражданской обороны. День МЧС 🚒",
    "05.10": "День работников уголовного розыска 🕵️, Всемирный день учителей 👩🏫",
    "06.10": "День российского страховщика 💼",
    "07.10": "День сотрудника штабных подразделений МВД 🛡️",
    "16.10": "День рождения Володиной Ирины 🎂",
    "17.10": "День рождения Каныгина Бориса 🎂",
    "18.10": "Предложение Зае 💍",
    "20.10": "День войск связи вооруженных сил РФ 📡, Международный день повара 👨🍳, Международный день авиадиспетчера ✈️",
    "23.10": "День работников рекламы 🖋️",
    "25.10": "День таможенника Российской Федерации 🛃",
    "28.10": "Всемирный день дзюдо 🥋",
    "29.10": "День работников службы вневедомственной охраны МВД 🛡️",
    "30.10": "День инженера-механика ⚙️, День рождения ВМФ России ⚓",
    "31.10": "День рождения Зайки 🎂, Хэллоуин 🎃",
    "01.11": "День судебного пристава ⚖️, День отца 👨",
    "04.11": "День народного единства в России 👫, День рождения Узлова Владимира 🎂",
    "05.11": "День военного разведчика 🕵️♂️",
    "10.11": "День сотрудников МВД России 🛡️",
    "11.11": "День экономиста 📊, День рождения Матвея Дручилова 🎂, День рождения Каныгиной Насти 🎂",
    "12.11": "День рождения Узловой Галины Васильевны 🎂",
    "13.11": "День войск РХБЗ России ☢️",
    "15.11": "День Каспийской флотилии ВМФ России ⚓, Всероссийский день призывника 🎖️",
    "16.11": "День рождения Каныгина Жени 🎂, День проектировщика 📐",
    "17.11": "День участковых уполномоченных полиции 👮, Международный день студентов 🎓",
    "19.11": "День рождения Каныгина Александра Александровича 🎂, День ракетных войск и артиллерии 🚀, День работника стекольной промышленности 🏭",
    "21.11": "День работника налоговых органов 💰",
    "22.11": "День психолога 🧠",
    "27.11": "День оценщика 💼, День морской пехоты ⚓",
    "30.11": "День матери 💐",
    "02.12": "День банковского работника 🏦",
    "03.12": "День неизвестного солдата 🕊️, День юриста ⚖️",
    "04.12": "День информатики 💻",
    "09.12": "День героев Отечества 🛡️, День ведомственной охраны ЖДТ 🚂",
    "12.12": "День Конституции РФ 📜",
    "16.12": "День ракетных войск стратегического назначения 🚀",
    "20.12": "День работника органов Государственной безопасности РФ 🛡️",
    "22.12": "День энергетика 💡",
    "27.12": "День спасателя Российской Федерации 🚒",
}


# Получение информации о праздниках
def get_holiday_info():
    """
    Возвращает информацию о сегодняшнем и ближайшем празднике.
    """
    today = datetime.now()
    today_date_str = today.strftime("%d.%m")

    # Проверяем, есть ли праздник сегодня
    holiday_today = HOLIDAYS.get(today_date_str)

    # Поиск ближайшего праздника
    holidays_sorted = sorted(
        HOLIDAYS.items(),
        key=lambda x: datetime.strptime(f"{x[0]}.{today.year}", "%d.%m.%Y")
    )
    nearest_holiday = None

    for date_str, name in holidays_sorted:
        holiday_date = datetime.strptime(f"{date_str}.{today.year}", "%d.%m.%Y")
        if holiday_date.date() > today.date():  # Ищем ближайший будущий праздник
            days_left = (holiday_date.date() - today.date()).days
            nearest_holiday = (name, holiday_date, days_left)
            break

    result = []
    if holiday_today:
        result.append(f"🎉 *Сегодня праздник:* {holiday_today}")
    if nearest_holiday and nearest_holiday[0] != holiday_today:
        name, holiday_date, days_left = nearest_holiday
        result.append(
            f"🎊 *Ближайший праздник:* {name} ({holiday_date.strftime('%d.%m.%Y')}) через {days_left} дн."
        )

    return "\n".join(result) if result else "🎉 Сегодня нет праздников."


# Пример вызова
if __name__ == "__main__":
    print(get_holiday_info())








