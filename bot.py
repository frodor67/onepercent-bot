import asyncio
import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from content_generator import generate_post
from aiogram.client.default import DefaultBotProperties

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

scheduler = AsyncIOScheduler()

# Времена публикации и темы
content_plan = {
    "06:00": "утренняя настройка",
    "12:00": "факт дня",
    "18:00": "микрочеллендж",
    "21:59": "вечерняя рефлексия"
}

async def send_post(topic: str):
    try:
        post_text = await generate_post(topic)  # <-- await обязательно!
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
        print(f"[{datetime.now()}] Sent post: {post_text[:40]}...")
    except Exception as e:
        print(f"❌ Error sending post: {e}")

async def scheduler_start():
    for time_str, topic in content_plan.items():
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_post, "cron", hour=hour, minute=minute, args=[topic])
    scheduler.start()

async def main():
    await scheduler_start()

    # ⏱ Моментальная отправка всех тем (или выбери нужные)
    print("🔔 Sending initial posts on startup...")
    await send_post("факт дня")

    print("✅ Bot is running and scheduler is active.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
