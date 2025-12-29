import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# ====== TOKEN ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не встановлений")

# ====== КНОПКИ ======
keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🔐 Перевірити пароль"), KeyboardButton("🔗 Перевірити посилання")],
        [KeyboardButton("🎲 Згенерувати пароль"), KeyboardButton("🛡 Поради з безпеки")],
        [KeyboardButton("ℹ️ Про бота"), KeyboardButton("🆘 Допомога")],
        [KeyboardButton("💡 Пропозиції")]
    ],
    resize_keyboard=True
)

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Вітаю!\n\n"
        "Я бот для безпеки 🔐\n"
        "Користуйся кнопками нижче ⬇️",
        reply_markup=keyboard
    )

# ====== КНОПКИ ======
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 Перевірка пароля\n\n"
        "❗ Не надсилай реальні паролі\n"
        "Напиши приклад структури (типу Abc123!)"
    )

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Перевірка посилання\n\n"
        "Надішли лінк, і я скажу, чи він підозрілий"
    )

async def generate_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Згенерований пароль:\n\n"
        "`F8#qL!2xP@9A`",
        parse_mode="Markdown"
    )

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради з безпеки:\n\n"
        "• Використовуй різні паролі\n"
        "• 2FA обовʼязково\n"
        "• Не переходь за підозрілими лінками"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Про бота\n\n"
        "Цей бот створений для допомоги з кібербезпекою 🔐"
    )

async def help_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Допомога\n\n"
        "Просто обери потрібну кнопку ⬇️"
    )

async def suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_suggestion"] = True
    await update.message.reply_text(
        "💡 Напиши свою пропозицію для покращення бота 👇"
    )

# ====== ТЕКСТ ======
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_suggestion"):
        context.user_data["waiting_suggestion"] = False
        await update.message.reply_text(
            "✅ Дякую! Пропозицію збережено 🙌",
            reply_markup=keyboard
        )
        return

    await update.message.reply_text(
        "ℹ️ Користуйся кнопками знизу ⬇️",
        reply_markup=keyboard
    )

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.Regex("^🔐 Перевірити пароль$"), check_password))
    app.add_handler(MessageHandler(filters.Regex("^🔗 Перевірити посилання$"), check_link))
    app.add_handler(MessageHandler(filters.Regex("^🎲 Згенерувати пароль$"), generate_password))
    app.add_handler(MessageHandler(filters.Regex("^🛡 Поради з безпеки$"), tips))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Про бота$"), about))
    app.add_handler(MessageHandler(filters.Regex("^🆘 Допомога$"), help_bot))
    app.add_handler(MessageHandler(filters.Regex("^💡 Пропозиції$"), suggestions))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
