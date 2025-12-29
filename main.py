import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== НАЛАШТУВАННЯ ==================
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ================== КНОПКИ ==================
main_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🔐 Перевірити пароль"), KeyboardButton("🔗 Перевірити посилання")],
        [KeyboardButton("🎲 Згенерувати пароль"), KeyboardButton("🛡 Поради з безпеки")],
        [KeyboardButton("ℹ️ Про бота"), KeyboardButton("🆘 Допомога")],
    ],
    resize_keyboard=True,
)

# ================== КОМАНДИ ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Я допоможу тобі з питаннями кібербезпеки 🔐\n"
        "Обери дію з меню нижче 👇",
        reply_markup=main_keyboard,
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — Запуск бота\n"
        "/password — Перевірка надійності пароля\n"
        "/link — Перевірка посилання\n"
        "/generate — Генерація пароля\n"
        "/tips — Поради з безпеки\n"
        "/about — Про бота\n"
        "/helpme — Допомога від спеціаліста"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Це бот з кібербезпеки.\n"
        "Він допоможе уникнути шахрайства та створити надійні паролі."
    )

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради з безпеки:\n"
        "• Не переходь за підозрілими посиланнями\n"
        "• Використовуй складні паролі\n"
        "• Не передавай коди нікому"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Приклад надійного пароля:\n"
        "`A9!fK2@Lm#8Q`",
        parse_mode="Markdown",
    )

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 Надішли пароль, і я підкажу чи він надійний."
    )

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Надішли посилання для перевірки на шахрайство."
    )

# ================== ДОПОМОГА ==================
user_help_requests = set()

async def helpme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_help_requests.add(update.effective_user.id)
    await update.message.reply_text(
        "🆘 Опиши свою проблему **одним повідомленням**.\n"
        "Я постараюся допомогти 👇"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id in user_help_requests:
        user_help_requests.remove(user_id)
        await update.message.reply_text(
            "✅ Дякую! Повідомлення отримано.\n"
            "Ми спробуємо допомогти найближчим часом 🙌"
        )
    else:
        await update.message.reply_text(
            "ℹ️ Скористайся кнопками меню або командою /help"
        )

# ================== ЗАПУСК ==================
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не заданий")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("tips", tips))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("password", password))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CommandHandler("helpme", helpme))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()

