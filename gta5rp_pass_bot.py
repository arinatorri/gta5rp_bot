
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_total_xp(level):
    return sum(1000 + i * 100 for i in range(level))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Привет! Я бот-калькулятор боевого пропуска GTA 5 RP 🌴
Напиши команду /calculate <уровень> <дата>, например:
/calculate 32 2025-06-06""")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        level = int(context.args[0])
        date_str = context.args[1]
        current_date = datetime.strptime(date_str, "%Y-%m-%d")

        current_xp = get_total_xp(level)
        final_xp = get_total_xp(100)
        remaining_xp = final_xp - current_xp
        days_needed = (remaining_xp + 5999) // 6000

        completion_date = current_date + timedelta(days=days_needed)

        await update.message.reply_text(
            f"Если вы на {level} уровне и сегодня {date_str}, то боевой пропуск завершится {completion_date.date()}"
        )
    except Exception:
        await update.message.reply_text("❌ Неверный формат. Используй: /calculate <уровень> <дата> (например, /calculate 32 2025-06-06)")

async def main():
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("calculate", calculate))
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
