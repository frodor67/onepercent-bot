import asyncio
import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from content_generator import generate_post

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
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
        post_text, image_path = await generate_post(topic)

        if image_path:
            with open(image_path, 'rb') as photo:
                await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=post_text)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=post_text)

        print(f"[{datetime.now()}] Sent post: {post_text[:40]}...")
    except Exception as e:
        print(f"Error sending post: {e}")

async def scheduler_start():
    for time_str, topic in content_plan.items():
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_post, "cron", hour=hour, minute=minute, args=[topic])
    scheduler.start()

async def main():
    print("\U0001F514 Sending initial posts on startup...")
    await send_post("факт дня")  # Пробный пост
    await scheduler_start()
    print("✅ Bot is running and scheduler is active.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
