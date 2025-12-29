import os
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот працює ✅")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
import os
import random
import string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ====== ТОКЕН ======
TOKEN = os.getenv("BOT_TOKEN")

# ====== ГОЛОВНЕ МЕНЮ (КНОПКИ ЗНИЗУ) ======
keyboard = [
    ["/password", "/generate"],
    ["/link", "/tips"],
    ["/help", "/about"]
]

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True
)

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n"
        "Я допоможу тобі з твоїм питанням з кібербезпеки 🔐\n\n"
        "Обери команду з меню знизу ⬇️",
        reply_markup=reply_keyboard
    )

# ====== /password ======
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔑 Перевірка надійності пароля\n\n"
        "Надішли пароль (я його не зберігаю), і я скажу, наскільки він надійний.",
        reply_markup=reply_keyboard
    )

# ====== /generate ======
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = "".join(random.choice(chars) for _ in range(12))

    await update.message.reply_text(
        f"🛡 Згенерований надійний пароль:\n\n`{password}`",
        parse_mode="Markdown",
        reply_markup=reply_keyboard
    )

# ====== /link ======
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Перевірка посилання на шахрайство\n\n"
        "Надішли посилання, і я допоможу визначити, чи воно підозріле.",
        reply_markup=reply_keyboard
    )

# ====== /tips ======
async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради з безпеки:\n"
        "1️⃣ Не переходь за підозрілими посиланнями\n"
        "2️⃣ Використовуй різні паролі\n"
        "3️⃣ Увімкни двофакторну автентифікацію\n"
        "4️⃣ Нікому не передавай коди доступу",
        reply_markup=reply_keyboard
    )

# ====== /about ======
async def about(update: Update, context: C

