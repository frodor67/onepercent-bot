# NOTE: This code requires a Python environment with full SSL and multiprocessing support.
# Ensure you're not using a minimal build (e.g., Alpine or some container builds).

import asyncio
import os
import ssl  # For SSL verification

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@onepercenistbetter")

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment")

try:
    import multiprocessing  # ensure _multiprocessing is available
    from multiprocessing import queues  # also triggers check for _multiprocessing
except ImportError as e:
    if '_multiprocessing' in str(e):
        raise ImportError("Your Python build lacks multiprocessing support (_multiprocessing). Use a full Python distribution.") from e
    raise

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
scheduler = AsyncIOScheduler()

# Контент шаблоны — можно вынести в отдельный JSON или подключить генератор
content_schedule = {
    "06:00": "\u2728 <b>1% Утренняя настройка</b>\nСегодня не нужно быть идеальным. Только лучше, чем вчера.",
    "12:00": "\ud83d\udcca <b>Факт дня</b>\n40% решений мы совершаем по привычке. Меняя одну, ты меняешь половину дня.",
    "18:00": "\ud83c\udfaf <b>Микрочеллендж</b>\n10 минут абсолютного фокуса.\nВыключи отвлечения. Просто начни.",
    "21:59": "\ud83c\udf1a <b>Рефлексия</b>\nЧто сегодня получилось? Что можно улучшить?\nЗавтра \u2014 снова на 1% вперёд."
}

async def send_post(text):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        print(f"Posted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {text[:30]}...")
    except Exception as e:
        print(f"Error posting: {e}")

async def scheduler_start():
    for time_str, message in content_schedule.items():
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_post, "cron", hour=hour, minute=minute, args=[message])
    scheduler.start()

async def main():
    await scheduler_start()
    print("Bot started and scheduler running...")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ModuleNotFoundError as e:
        if 'ssl' in str(e):
            print("\nERROR: Your Python environment does not include SSL support.\nPlease install a full version of Python (not a stripped-down build).\n")
        elif '_multiprocessing' in str(e):
            print("\nERROR: Your Python is missing _multiprocessing module.\nUse an official full Python build (e.g., python:3.12 or python.org installer).\n")
        raise
