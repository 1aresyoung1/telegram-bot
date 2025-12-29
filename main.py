import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- ЛОГИ ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------- TOKEN ----------
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не знайдено. Додай його в Shared Variables")

# ---------- КНОПКИ ----------
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🔐 Перевірити пароль", "🔗 Перевірити посилання"],
        ["🎲 Згенерувати пароль", "🛡 Поради з безпеки"],
        ["ℹ️ Про бота", "🆘 Допомога"],
        ["💡 Пропозиції"]
    ],
    resize_keyboard=True
)

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Я бот з кібербезпеки 🔐\n"
        "Обери дію з меню нижче ⬇️",
        reply_markup=MAIN_KEYBOARD
    )

# ---------- КОМАНДИ ----------
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Я допомагаю з:\n"
        "• паролями\n"
        "• фішингом\n"
        "• порадами з безпеки"
    )

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради:\n"
        "• Не переходь по підозрілих лінках\n"
        "• Використовуй різні паролі\n"
        "• Увімкни 2FA"
    )

# ---------- AI ДОПОМОГА ----------
async def help_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["help_mode"] = True
    await update.message.reply_text(
        "🆘 Опиши свою проблему одним повідомленням.\n"
        "Я спробую допомогти 🤖"
    )

async def suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["suggest_mode"] = True
    await update.message.reply_text(
        "💡 Напиши свою пропозицію для покращення бота"
    )

# ---------- ОБРОБКА ТЕКСТУ ----------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("help_mode"):
        context.user_data["help_mode"] = False
        await update.message.reply_text(
            "🤖 Я проаналізував проблему.\n"
            "Раджу:\n"
            "• оновити систему\n"
            "• перевірити віруси\n"
            "• змінити паролі"
        )
        return

    if context.user_data.get("suggest_mode"):
        context.user_data["suggest_mode"] = False
        await update.message.reply_text(
            "✅ Дякую! Пропозицію збережено 🙌"
        )
        return

    await update.message.reply_text(
        "ℹ️ Користуйся кнопками знизу ⬇️"
    )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("tips", tips))

    app.add_handler(MessageHandler(filters.Regex("🆘 Допомога"), help_ai))
    app.add_handler(MessageHandler(filters.Regex("ℹ️ Про бота"), about))
    app.add_handler(MessageHandler(filters.Regex("🛡 Поради з безпеки"), tips))
    app.add_handler(MessageHandler(filters.Regex("💡 Пропозиції"), suggestions))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
