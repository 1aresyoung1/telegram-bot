import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔴 ВСТАВ СВІЙ ТОКЕН ТУТ
TOKEN = "PASTE_YOUR_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)

# --- КНОПКИ ---
keyboard = ReplyKeyboardMarkup(
    [
        ["password", "generate"],
        ["link", "tips"],
        ["about", "help"],
        ["helpme"],
    ],
    resize_keyboard=True,
)

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\nЯ допоможу тобі з твоїми питаннями з безпеки 🔐",
        reply_markup=keyboard,
    )

# --- /password ---
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔑 Надійний пароль має:\n• 8+ символів\n• великі і малі літери\n• цифри\n• спецсимволи"
    )
