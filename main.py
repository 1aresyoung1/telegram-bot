from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU")  # токен задай у Railway → Variables

# --- AI логіка ---
def ai_answer(text: str) -> str:
    text = text.lower()

    if "краш" in text or "не працює" in text or "помилка" in text:
        return "⚠️ Схоже на технічну помилку.\nСпробуй перезапустити додаток та перевір інтернет."

    if "злам" in text or "хак" in text:
        return "🚨 Є ризик злому.\nНегайно зміни паролі та увімкни двофакторну автентифікацію."

    if "фішинг" in text or "підозріле посилання" in text:
        return "🔗 Не переходь за цим посиланням.\nПеревір URL та не вводь особисті дані."

    if "пароль" in text:
        return "🔐 Пароль має бути довгим, унікальним та містити цифри й символи."

    return (
        "🤖 Я поки не впевнений у відповіді.\n"
        "Твоє повідомлення буде передано спеціалісту 🙌"
    )

# --- Команди ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔐 password", "🔗 link"],
        ["🎲 generate", "📘 tips"],
        ["ℹ️ about", "🆘 helpme"]
    ]
    await update.message.reply_text(
        "👋 Привіт! Я допоможу тобі з питаннями безпеки.\nОбери команду ⬇️",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def helpme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["help_mode"] = True
    await update.message.reply_text(
        "🆘 Опиши свою проблему одним повідомленням.\nЯ спробую допомогти 🤖"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("help_mode"):
        user_text = update.message_
