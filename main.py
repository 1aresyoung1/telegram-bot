import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU"

logging.basicConfig(level=logging.INFO)

# 🎨 ГАРНЕ МЕНЮ
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🔐 Перевірити пароль", "🎲 Згенерувати пароль"],
        ["🔗 Перевірити лінк", "🛡 Поради"],
        ["ℹ️ Про бота", "❓ Команди"],
        ["🆘 Допомога"],
    ],
    resize_keyboard=True,
)

# 🟢 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Я допоможу тобі з питаннями кібербезпеки 🔐\n"
        "Обери дію з меню нижче 👇",
        reply_markup=MAIN_KEYBOARD,
    )

# 🔐 Перевірка пароля
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔑 Надійний пароль має:\n"
        "• 8+ символів\n"
        "• великі та малі літери\n"
        "• цифри\n"
        "• спецсимволи (!@#$)"
    )

# 🎲 Генерація
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Приклад надійного пароля:\n\n`A9!kQ7@zP2`",
        parse_mode="Markdown",
    )

# 🔗 Фішинг
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Приклад фішингового посилання:\n"
        "http://paypaI-secure-login.com\n\n"
        "Зверни увагу на букву **I**, а не **l**"
    )

# 🛡 Поради
async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради:\n"
        "• Не переходь за підозрілими лінками\n"
        "• Нікому не передавай код з SMS\n"
        "• Використовуй 2FA"
    )

# ℹ️ Про бота
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Цей бот допомагає навчитись основам кібербезпеки."
    )

# ❓ Команди
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Доступні команди:\n\n"
        "/start — Головне меню\n"
        "🔐 Перевірити пароль\n"
        "🎲 Згенерувати пароль\n"
        "🔗 Перевірити лінк\n"
        "🛡 Поради\n"
        "🆘 Допомога"
    )

# 🆘 HELP ME (ПРАЦЮЄ)
async def helpme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_help"] = True
    await update.message.reply_text(
        "🆘 Опиши свою проблему одним повідомленням.\n"
        "Я передам її для допомоги 👇"
    )

# 💬 ТЕКСТ
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("waiting_help"):
        context.user_data["waiting_help"] = False
        await update.message.reply_text(
            "✅ Дякую! Твоє повідомлення отримано.\n"
            "Ми спробуємо допомогти найближчим часом 🙌"
        )
        return

    if text == "🔐 Перевірити пароль":
        await password(update, context)
    elif text == "🎲 Згенерувати пароль":
        await generate(update, context)
    elif text == "🔗 Перевірити лінк":
        await link(update, context)
    elif text == "🛡 Поради":
        await tips(update, context)
    elif text == "ℹ️ Про бота":
        await about(update, context)
    elif text == "❓ Команди":
        await help_cmd(update, context)
    elif text == "🆘 Допомога":
        await helpme(update, context)
    else:
        await update.message.reply_text(
            "❗ Я не зрозумів повідомлення.\n"
            "Скористайся меню 👇"
        )

# 🚀 MAIN
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
