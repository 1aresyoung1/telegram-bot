import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("8596592294:AAHvoj-GVwfToT103XWOcvMMUoqE2DrkflU")

logging.basicConfig(level=logging.INFO)

# ====== КНОПКИ ======
keyboard = ReplyKeyboardMarkup(
    [
        ["🔐 Перевірити пароль", "🔗 Перевірити посилання"],
        ["🎲 Згенерувати пароль", "🛡 Поради з безпеки"],
        ["ℹ️ Про бота", "🆘 Допомога"],
    ],
    resize_keyboard=True,
)

waiting_for_problem = set()

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n"
        "Я допоможу тобі з питаннями кібербезпеки 🔐\n"
        "Обери дію з меню нижче 👇",
        reply_markup=keyboard,
    )

# ====== КНОПКИ ======
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🔐 Перевірити пароль":
        await update.message.reply_text(
            "🔐 Надішли пароль, я скажу чи він надійний."
        )

    elif text == "🔗 Перевірити посилання":
        await update.message.reply_text(
            "🔗 Надішли посилання, я перевірю чи воно безпечне."
        )

    elif text == "🎲 Згенерувати пароль":
        await update.message.reply_text(
            "🎲 Ось приклад надійного пароля:\n`X9!aQ2#Lm@7F`",
            parse_mode="Markdown",
        )

    elif text == "🛡 Поради з безпеки":
        await update.message.reply_text(
            "🛡 Поради:\n"
            "• Не переходь за підозрілими посиланнями\n"
            "• Не передавай коди\n"
            "• Використовуй унікальні паролі"
        )

    elif text == "ℹ️ Про бота":
        await update.message.reply_text(
            "ℹ️ Це бот з кібербезпеки.\n"
            "Він допомагає захистити твої дані."
        )

    elif text == "🆘 Допомога":
        waiting_for_problem.add(user_id)
        await update.message.reply_text(
            "🆘 Опиши свою проблему **одним повідомленням**.\n"
            "Я спробую допомогти 👇"
        )

    else:
        # ====== ШІ ВІДПОВІДЬ ======
        if user_id in waiting_for_problem:
            waiting_for_problem.remove(user_id)
            answer = ai_answer(text)
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text(
                "ℹ️ Обери дію з меню 👇"
            )

# ====== ПРОСТИЙ ШІ (локальний) ======
def ai_answer(problem: str) -> str:
    p = problem.lower()

    if "вірус" in p or "злам" in p:
        return (
            "🚨 Схоже на загрозу безпеці.\n"
            "Рекомендую:\n"
            "• Змінити всі паролі\n"
            "• Увімкнути 2FA\n"
            "• Перевірити пристрій антивірусом"
        )

    if "посилання" in p or "сайт" in p:
        return (
            "🔗 Якщо посилання виглядає підозріло:\n"
            "• Не вводь дані\n"
            "• Перевір домен\n"
            "• Краще не відкривати"
        )

    if "пароль" in p:
        return (
            "🔐 Надійний пароль має:\n"
            "• 12+ символів\n"
            "• Великі/малі літери\n"
            "• Цифри та символи"
        )

    return (
        "🤖 Я проаналізував проблему.\n"
        "Рекомендую діяти обережно та не передавати особисті дані.\n"
        "Якщо хочеш — уточни деталі."
    )

# ====== ЗАПУСК ======
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

    app.run_polling()

if __name__ == "__main__":
    main()
