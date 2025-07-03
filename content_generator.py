import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_post(topic: str) -> str:
    prompt = f"Напиши вдохновляющий короткий пост для телеграм-канала о личной эффективности. Тема: {topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]
