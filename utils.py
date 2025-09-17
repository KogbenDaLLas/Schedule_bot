import datetime

RU_MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]

RU_WEEKDAYS = [
    "Понедельник", "Вторник", "Среда",
    "Четверг", "Пятница", "Суббота", "Воскресенье"
]

START_DATE = datetime.date(2025, 9, 15)  # Первая учебная неделя

def current_week_type() -> int:
    today = datetime.date.today()
    delta_weeks = (today - START_DATE).days // 7
    return delta_weeks % 2

def next_date_for_weekday(day_name: str) -> datetime.date:

    days_map = {
        "понедельник": 0,
        "вторник": 1,
        "среда": 2,
        "четверг": 3,
        "пятница": 4,
        "суббота": 5,
        "воскресенье": 6
    }

    target = days_map[day_name.lower()]
    today = datetime.date.today()
    # weekday(): Monday=0, Sunday=6
    delta = (target - today.weekday()) % 7
    return today + datetime.timedelta(days=delta)

def format_day(lessons: list[dict], day_name: str) -> str:
    date_for_day = next_date_for_weekday(day_name)

    weekday_str = RU_WEEKDAYS[date_for_day.weekday()]
    month_str = RU_MONTHS[date_for_day.month - 1]
    date_str = f"{date_for_day.day} {month_str} {date_for_day.year}"

    header = f"*{weekday_str}, {date_str}*\n\n"
    blocks = []
    for l in lessons:
        block = (
            f"📚 {l['subject']}\n"
            f"🕒 {l['time']}\n"
            f"📍 {l['location']}\n"
        )
        blocks.append(block)
    return header + "\n".join(blocks)
