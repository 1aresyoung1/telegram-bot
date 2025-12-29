import os
import random
import string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ===== TOKEN =====
TOKEN = os.getenv("BOT_TOKEN")

# ===== MENU BUTTONS =====
keyboard = [
    ["/password", "/generate"],
    ["/link", "/tips"],
    ["/help", "/about"]
]

menu = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n"
        "Я допоможу тобі з твоїм питанням з кібербезпеки 🔐\n\n"
        "Обери команду з меню знизу ⬇️",
        reply_markup=menu
    )

# ===== PASSWORD CHECK =====
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "password"
    await update.message.reply_text(
        "🔑 Надішли пароль, і я перевірю його надійність",
        reply_markup=menu
    )

# ===== LINK CHECK =====
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "link"
    await update.message.reply_text(
        "🔗 Надішли посилання, і я скажу, чи воно підозріле",
        reply_markup=menu
    )

# ===== PASSWORD GENERATOR =====
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    pwd = "".join(random.choice(chars) for _ in range(12))
    await update.message.reply_text(
        f"🛡 Згенерований надійний пароль:\n\n`{pwd}`",
        parse_mode="Markdown",
        reply_markup=menu
    )

# ===== TIPS =====
async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Поради з безпеки:\n"
        "1️⃣ Не переходь за підозрілими посиланнями\n"
        "2️⃣ Використовуй різні паролі\n"
        "3️⃣ Увімкни 2FA\n"
        "4️⃣ Нікому не передавай коди",
        reply_markup=menu
    )

# ===== ABOUT =====
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Я бот з кібербезпеки.\n"
        "Допомагаю перевіряти паролі та посилання 🔐",
        reply_markup=menu
    )

# ===== HELP =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Команди бота:\n\n"
        "/start — Запуск і меню\n"
        "/password — Перевірка пароля\n"
        "/link — Перевірка посилання\n"
        "/generate — Генерація пароля\n"
        "/tips — Поради з безпеки\n"
        "/about — Про бота\n"
        "/help — Допомога",
        reply_markup=menu
    )

# ===== TEXT HANDLER =====
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")

    if mode == "password":
        pwd = update.message.text
        score = sum([
            len(pwd) >= 8,
            any(c.isdigit() for c in pwd),
            any(c.isupper() for c in pwd),
            any(c in "!@#$%^&*()" for c in pwd)
        ])

        levels = ["❌ Дуже слабкий", "⚠️ Слабкий", "🙂 Середній", "✅ Надійний", "🔒 Дуже надійний"]
        await update.message.reply_text(
            f"Результат: {levels[score]}",
            reply_markup=menu
        )
        context.user_data.clear()

    elif mode == "link":
        url = update.message.text
        if any(x in url.lower() for x in ["bit.ly", "tinyurl", "@", "//login"]):
            result = "⚠️ Посилання виглядає ПІДОЗРІЛИМ"
        else:
            result = "✅ Посилання виглядає безпечним"
        await update.message.reply_text(result, reply_markup=menu)
        context.user_data.clear()

# ===== MAIN =====
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("password", password))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("tips", tips))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()

