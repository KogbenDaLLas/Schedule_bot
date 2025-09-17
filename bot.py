from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from schedule import schedule
from utils import current_week_type, format_day
from dotenv import load_dotenv
import os

def day_keyboard() -> InlineKeyboardMarkup:
    days = [
        ("ПН 😰", "Понедельник"),
        ("ВТ 😐", "Вторник"),
        ("СР 🙂", "Среда"),
        ("ЧТ 😏", "Четверг"),
        ("ПТ 😃", "Пятница"),
        ("СБ 🥳", "Суббота"),
    ]
    # Две кнопки в ряд
    buttons = [
        [InlineKeyboardButton(text, callback_data=f"day_{key}")
         for text, key in days[i:i + 2]]
        for i in range(0, len(days), 2)
    ]
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите день недели:",
        reply_markup=day_keyboard()
    )

# Определяем день недели
async def show_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    day_key = query.data.replace("day_", "")
    week_type = current_week_type()
    lessons = schedule.get(week_type, {}).get(day_key, [])

    if not lessons:
        text = f"*{day_key.title()}*\n\nЗанятий нет."
    else:
        text = format_day(lessons, day_key)

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=day_keyboard()
    )

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_day, pattern="^day_"))

    app.run_polling()

if __name__ == "__main__":
    main()
