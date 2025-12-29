import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =======================
# НАЛАШТУВАННЯ
# =======================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =======================
# КНОПКИ МЕНЮ
# =======================
menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🔐 Перевірити пароль"), KeyboardButton("🔗 Перевірити посилання")],
        [KeyboardButton("🎲 Згенерувати пароль"), KeyboardButton("🛡 Поради з безпеки")],
        [KeyboardButton("ℹ️ Про бота"), KeyboardButton("🆘 Допомог]()
