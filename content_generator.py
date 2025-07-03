import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def generate_post(topic: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    json_data = {
        "model": "gpt-4o-mini",  # или другая доступная модель
        "messages": [
            {"role": "system", "content": "Ты бот, генерирующий короткие интересные посты."},
            {"role": "user", "content": f"Создай пост на тему: {topic}"}
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=json_data)
    if response.status_code != 200:
        raise Exception(f"Ошибка генерации контента: {response.status_code} - {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]


# import os
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from PIL import Image
# from io import BytesIO
# import aiohttp

# load_dotenv()

# client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# async def generate_post(topic: str) -> tuple[str, str | None]:
#     try:
#         # 1. Генерируем текст поста
#         chat_response = await client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "Ты пишешь вдохновляющие, короткие посты в Telegram-канал в стиле лайфкоуча. Каждый пост — отдельная мысль или мотивация."},
#                 {"role": "user", "content": f"Напиши пост на тему: {topic}"}
#             ],
#             temperature=0.7
#         )

#         text = chat_response.choices[0].message.content.strip()

#         # 2. Генерируем картинку по теме
#         image_prompt = f"Иллюстрация к посту на тему: {topic}, эстетичная, минималистичная, вдохновляющая"
#         image_response = await client.images.generate(
#             model="dall-e-3",
#             prompt=image_prompt,
#             size="1024x1024",
#             quality="standard",
#             n=1
#         )

#         image_url = image_response.data[0].url

#         # 3. Загружаем изображение в память и сохраняем на диск
#         async with aiohttp.ClientSession() as session:
#             async with session.get(image_url) as resp:
#                 if resp.status == 200:
#                     image_bytes = await resp.read()
#                     image = Image.open(BytesIO(image_bytes))
#                     image_path = f"generated_image_{topic.replace(' ', '_')}.png"
#                     image.save(image_path)
#                     return text, image_path
#                 else:
#                     print(f"Ошибка загрузки изображения: {resp.status}")
#                     return text, None

#     except Exception as e:
#         print(f"Ошибка при генерации контента: {e}")
#         return "Произошла ошибка при генерации поста.", None
