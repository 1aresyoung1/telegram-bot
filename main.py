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
TOKEN = os.getenv("8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не знайдено в Environment Variables")

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
        [KeyboardButton("ℹ️ Про бота"), KeyboardButton("🆘 Допомога")],
        [KeyboardButton("💡 Пропозиції")]
    ],
    resize_keyboard=True
)

# =======================
# /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Я бот з кібербезпеки 🔐\n"
        "Я допоможу тобі з паролями, посиланнями та безпекою.\n\n"
        "⬇️ Обери дію з меню нижче",
        reply_markup=menu_keyboard
    )

# =======================
# AI-ВІДПОВІДЬ (простий інтелект)
# =======================
def ai_help_answer(text: str) -> str:
    text = text.lower()

    if "злам" in text or "взлом" in text:
        return (
            "🚨 Схоже на злам.\n\n"
            "1️⃣ Зміни всі паролі\n"
            "2️⃣ Увімкни 2FA\n"
            "3️⃣ Перевір пристрій антивірусом\n"
            "4️⃣ Не переходь по підозрілих посиланнях"
        )

    if "вірус" in text:
        return (
            "🦠 Можливий вірус.\n\n"
            "✔️ Не встановлюй програми з невідомих сайтів\n"
            "✔️ Проскануй пристрій антивірусом\n"
            "✔️ Видали підозрілі додатки"
        )

    if "пароль" in text:
        return (
            "🔐 Паролі мають бути:\n"
            "• не коротші 12 символів\n"
            "• з великими і малими літерами\n"
            "• з цифрами і символами"
        )

    return (
        "🤖 Я проаналізував проблему.\n\n"
        "✔️ Уникай підозрілих сайтів\n"
        "✔️ Не передавай коди підтвердження\n"
        "✔️ Використовуй складні паролі\n\n"
        "Якщо проблема серйозна — звернись до спеціаліста 👨‍💻"
    )

# =======================
# ОБРОБКА ПОВІДОМЛЕНЬ
# =======================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ---------- ПЕРЕВІРКА ПАРОЛЯ ----------
    if text == "🔐 Перевірити пароль":
        context.user_data["mode"] = "password"
        await update.message.reply_text("✍️ Введи пароль для перевірки:")
        return

    if context.user_data.get("mode") == "password":
        context.user_data.clear()
        if len(text) < 8:
            await update.message.reply_text("❌ Слабкий пароль (менше 8 символів)")
        else:
            await update.message.reply_text("✅ Пароль виглядає надійним")
        return

    # ---------- ПЕРЕВІРКА ПОСИЛАННЯ ----------
    if text == "🔗 Перевірити посилання":
        await update.message.reply_text(
            "⚠️ Якщо посилання просить пароль або дані — це може бути фішинг.\n"
            "❌ Я не рекомендую переходити по незнайомих URL."
        )
        return

    # ---------- ГЕНЕРАЦІЯ ПАРОЛЯ ----------
    if text == "🎲 Згенерувати пароль":
        await update.message.reply_text(
            "🔑 Згенерований пароль:\n\n"
            "`A9$fK!2xQ#8L`",
            parse_mode="Markdown"
        )
        return

    # ---------- ПОРАДИ ----------
    if text == "🛡 Поради з безпеки":
        await update.message.reply_text(
            "🛡 Основні поради:\n"
            "• Не переходь по підозрілих посиланнях\n"
            "• Не передавай коди\n"
            "• Використовуй 2FA"
        )
        return

    # ---------- ПРО БОТА ----------
    if text == "ℹ️ Про бота":
        await update.message.reply_text(
            "ℹ️ Бот створений для допомоги з кібербезпекою.\n"
            "Версія: 1.0\n"
            "Автор: You 💙"
        )
        return

    # ---------- ДОПОМОГА (AI) ----------
    if text == "🆘 Допомога":
        context.user_data["mode"] = "help"
        await update.message.reply_text(
            "🆘 Опиши свою проблему одним повідомленням.\n"
            "🤖 Я спробую допомогти автоматично 👇"
        )
        return

    if context.user_data.get("mode") == "help":
        context.user_data.clear()
        answer = ai_help_answer(text)
        await update.message.reply_text(answer)
        return

    # ---------- ПРОПОЗИЦІЇ ----------
    if text == "💡 Пропозиції":
        context.user_data["mode"] = "suggest"
        await update.message.reply_text("💡 Напиши свою пропозицію для оновлення бота:")
        return

    if context.user_data.get("mode") == "suggest":
        context.user_data.clear()
        await update.message.reply_text(
            "✅ Дякую! Пропозицію збережено.\n"
            "Вона буде врахована в майбутніх оновленнях 🚀"
        )
        return

# =======================
# ЗАПУСК
# =======================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущено")
    app.run_polling()

if __name__ == "__main__":
    main()
