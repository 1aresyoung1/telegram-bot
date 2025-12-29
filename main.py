import os
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# ===== TOKEN =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не встановлений")

# ===== KEYBOARD =====
keyboard = ReplyKeyboardMarkup(
    [
        ["🔐 Перевірити пароль", "🔗 Перевірити посилання"],
        ["🎲 Згенерувати пароль", "🛡 Поради з безпеки"],
        ["ℹ️ Про бота", "🆘 Допомога"],
        ["💡 Пропозиції"]
    ],
    resize_keyboard=True
)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Вітаю!\n\n"
        "Я бот з кібербезпеки 🔐\n"
        "Можеш писати або користуватись кнопками ⬇️",
        reply_markup=keyboard
    )

# ===== BUTTON HANDLERS =====
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "password"
    await update.message.reply_text(
        "🔐 Перевірка пароля\n\n"
        "❗ Не надсилай реальні паролі\n"
        "Напиши приклад (типу Abc123!)"
    )

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "link"
    await update.message.reply_text(
        "🔗 Перевірка посилання\n\n"
        "Надішли URL для перевірки"
    )

async def generate_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🎲 Згенерований пароль:\n\n"
        "`F8#qL!2xP@9A`",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🛡 Поради з безпеки:\n\n"
        "• Різні паролі\n"
        "• 2FA\n"
        "• Не відкривай підозрілі лінки",
        reply_markup=keyboard
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "ℹ️ Про бота\n\n"
        "Бот допомагає з базовою кібербезпекою 🔐",
        reply_markup=keyboard
    )

async def help_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🆘 Допомога\n\n"
        "Обери кнопку або напиши текст",
        reply_markup=keyboard
    )

async def suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "suggestion"
    await update.message.reply_text(
        "💡 Напиши свою пропозицію 👇"
    )

# ===== TEXT HANDLER =====
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    # --- PASSWORD CHECK ---
    if mode == "password":
        context.user_data.clear()

        strength = 0
        if len(text) >= 8: strength += 1
        if re.search(r"[A-Z]", text): strength += 1
        if re.search(r"[a-z]", text): strength += 1
        if re.search(r"[0-9]", text): strength += 1
        if re.search(r"[!@#$%^&*]", text): strength += 1

        if strength <= 2:
            result = "🔴 Слабкий пароль"
        elif strength <= 4:
            result = "🟡 Середній пароль"
        else:
            result = "🟢 Надійний пароль"

        await update.message.reply_text(
            f"🔐 Результат:\n{result}",
            reply_markup=keyboard
        )
        return

    # --- LINK CHECK ---
    if mode == "link":
        context.user_data.clear()
        if text.startswith("http"):
            await update.message.reply_text(
                "🔍 Посилання виглядає коректно\n(це не гарантія безпеки)",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                "❌ Це не схоже на посилання",
                reply_markup=keyboard
            )
        return

    # --- SUGGESTION ---
    if mode == "suggestion":
        context.user_data.clear()
        await update.message.reply_text(
            "✅ Дякую! Пропозицію збережено 🙌",
            reply_markup=keyboard
        )
        return

    # --- DEFAULT ---
    await update.message.reply_text(
        "ℹ️ Обери дію кнопками знизу ⬇️",
        reply_markup=keyboard
    )

# ===== MAIN =====
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

    app.run_polling()

if __name__ == "__main__":
    main()
