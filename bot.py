import asyncio
import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@onepercenistbetter")

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment")

# Проверка multiprocessing — для стабильности на лёгких сборках
try:
    import multiprocessing
except ImportError:
    print("⚠️ WARNING: multiprocessing не доступен. APScheduler может работать не полностью.")

# Бот и планировщик
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
scheduler = AsyncIOScheduler()

# Расписание публикаций
content_schedule = {
    "06:00": "✨ <b>1% Утренняя настройка</b>\nСегодня не нужно быть идеальным. Только лучше, чем вчера.",
    "12:00": "📊 <b>Факт дня</b>\n40% решений мы совершаем по привычке. Меняя одну, ты меняешь половину дня.",
    "18:00": "🎯 <b>Микрочеллендж</b>\n10 минут абсолютного фокуса.\nВыключи отвлечения. Просто начни.",
    "21:59": "🌚 <b>Рефлексия</b>\nЧто сегодня получилось? Что можно улучшить?\nЗавтра — снова на 1% вперёд."
}

async def send_post(text: str):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Отправлено: {text[:30]}...")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")

async def scheduler_start():
    for time_str, message in content_schedule.items():
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_post, "cron", hour=hour, minute=minute, args=[message])
    scheduler.start()

async def main():
    await scheduler_start()
    print("✅ Бот запущен и планировщик работает...")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ModuleNotFoundError as e:
        if 'ssl' in str(e):
            print("🚨 Ошибка: отсутствует SSL. Используйте полноценную сборку Python.")
        elif '_multiprocessing' in str(e):
            print("🚨 Ошибка: отсутствует _multiprocessing. Используйте python:3.11-slim или официальный билд.")
        raise
