
import os
import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

# Состояния диалога
LEVEL, DATE = range(2)

def get_total_xp(level):
    return sum(1000 + i * 100 for i in range(level))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я помогу рассчитать дату завершения боевого пропуска GTA 5 RP.

Сначала скажи, какой у тебя сейчас уровень?")
    return LEVEL

async def get_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        level = int(update.message.text)
        if level < 1 or level > 100:
            raise ValueError
        context.user_data["level"] = level
        await update.message.reply_text("📅 Теперь введи сегодняшнюю дату в формате ГГГГ-ММ-ДД (например, 2025-06-11):")
        return DATE
    except ValueError:
        await update.message.reply_text("❌ Введи корректное число от 1 до 100.")
        return LEVEL

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        level = context.user_data["level"]
        date_str = update.message.text
        current_date = datetime.strptime(date_str, "%Y-%m-%d")

        current_xp = get_total_xp(level)
        final_xp = get_total_xp(100)
        remaining_xp = final_xp - current_xp
        days_needed = (remaining_xp + 5999) // 6000

        completion_date = current_date + timedelta(days=days_needed)
        await update.message.reply_text(
            f"✅ Если вы на {level} уровне и сегодня {date_str},\nто боевой пропуск завершится **{completion_date.date()}**.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    except Exception:
        await update.message.reply_text("❌ Введи дату в правильном формате: ГГГГ-ММ-ДД (например, 2025-06-11).")
        return DATE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Диалог отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def main():
    from nest_asyncio import apply
    apply()

    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_level)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    await app.run_polling()

if __name__ == '__main__':
    import asyncio

    try:
        asyncio.run(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
