# NOTE: This code requires a full-featured Python environment with SSL and multiprocessing support.
# Avoid minimal builds like Alpine Linux without glibc or musl patching.

import asyncio
import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@onepercenistbetter")

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment")

# Fallback scheduler if multiprocessing is unavailable
use_basic_scheduler = False

try:
    import multiprocessing
    from multiprocessing import queues
except ImportError:
    print("WARNING: Python build lacks full multiprocessing support. Switching to basic scheduler mode.")
    use_basic_scheduler = True

# Bot and Scheduler setup
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
scheduler = AsyncIOScheduler()

# Content messages mapped to posting time
content_schedule = {
    "06:00": "✨ <b>1% Утренняя настройка</b>\nСегодня не нужно быть идеальным. Только лучше, чем вчера.",
    "12:00": "📊 <b>Факт дня</b>\n40% решений мы совершаем по привычке. Меняя одну, ты меняешь половину дня.",
    "18:00": "🎯 <b>Микрочеллендж</b>\n10 минут абсолютного фокуса.\nВыключи отвлечения. Просто начни.",
    "21:59": "🌚 <b>Рефлексия</b>\nЧто сегодня получилось? Что можно улучшить?\nЗавтра — снова на 1% вперёд."
}

async def send_post(text: str):
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
            print("\nERROR: Your Python environment lacks SSL support. Please use a standard Python build.\n")
        elif '_multiprocessing' in str(e):
            print("\nERROR: Your Python lacks _multiprocessing. Use python:3.12-slim or official python.org installer.\n")
        raise
    except RuntimeError as e:
        print(f"Runtime error: {e}")
