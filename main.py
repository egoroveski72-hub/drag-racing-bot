import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncioScheduler

# Дані вашого бота
TOKEN = "8588338178:AAEJAJkzVUVrf_3ZPsOYSNsDuOTQwPC0Ffc"
GROUP_ID = -1002447990040 

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncioScheduler(timezone="Europe/Kyiv")

async def market_alert():
    await bot.send_message(GROUP_ID, "🔄 **ОНОВЛЕННЯ РИНКУ!**\nПеревірте нові товари!")

async def race_alert():
    await bot.send_message(GROUP_ID, "🏎️ **ЧАС ГОНКИ!**\nВсі на старт, прогріваємо гуму!")

async def boss_alert():
    await bot.send_message(GROUP_ID, "👹 **ЧАС БОСА!**\nЗаходимо в гру, б'ємо боса всією командою!")

@dp.message(Command("id"))
async def get_id(message: types.Message):
    await message.answer(f"ID цієї групи: `{message.chat.id}`")

def setup_schedule():
    # Налаштування часу (можна змінити цифри годин)
    scheduler.add_job(market_alert, "cron", hour="0,4,8,12,16,20", minute=0)
    scheduler.add_job(race_alert, "cron", hour=19, minute=0)
    scheduler.add_job(boss_alert, "cron", hour=21, minute=0)

async def main():
    logging.basicConfig(level=logging.INFO)
    setup_schedule()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
