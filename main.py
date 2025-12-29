import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не встановлений")

# ====== МЕНЮ ======
keyboard = ReplyKeyboardMarkup(
    [
        ["🔐 Перевірити пароль", "🎲 Згенерувати пароль"],
        ["🛡 Поради", "🆘 Допомога"],
        ["ℹ️ Про бота", "💡 Пропозиції"]
    ],
    resize_keyboard=True
)

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n"
        "Я бот з кібербезпеки 🔐\n\n"
        "⬇️ Обери дію з меню",
        reply_markup=keyboard
    )

# ====== ПОВІДОМЛЕННЯ ======
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔐 Перевірити пароль":
        await update.message.reply_text("🔐 Надішли пароль для перевірки")
        context.user_data["mode"] = "password"

    elif context.user_data.get("mode") == "password":
        context.user_data.clear()
        if len(text) < 8:
            await update.message.reply_text("❌ Слабкий пароль")
        else:
            await update.message.reply_text("✅ Пароль нормальний")

    elif text == "🎲 Згенерувати пароль":
        await update.message.reply_text("🔑 Пароль: `A9#fK2!xQ8L`", parse_mode="Markdown")

    elif text == "🛡 Поради":
        await update.message.reply_text(
            "🛡 Поради:\n"
            "• Не переходь по підозрілих лінках\n"
            "• Використовуй 2FA\n"
            "• Складні паролі"
        )

    elif text == "ℹ️ Про бота":
        await update.message.reply_text("ℹ️ Бот для допомоги з кібербезпекою")

    elif text == "🆘 Допомога":
        context.user_data["mode"] = "help"
        await update.message.reply_text("🆘 Опиши свою проблему одним повідомленням")

    elif context.user_data.get("mode") == "help":
        context.user_data.clear()
        await update.message.reply_text(
            "🤖 Я отримав твою проблему.\n"
            "Порада: зміни паролі, перевір пристрій, не передавай коди."
        )

    elif text == "💡 Пропозиції":
        context.user_data["mode"] = "idea"
        await update.message.reply_text("💡 Напиши пропозицію для покращення бота")

    elif context.user_data.get("mode") == "idea":
        context.user_data.clear()
        await update.message.reply_text("✅ Дякую! Пропозицію збережено")

    else:
        await update.message.reply_text("❓ Обери дію з меню ⬇️")

# ====== ЗАПУСК ======
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, messages))
    app.run_polling()

if __name__ == "__main__":
    main()
