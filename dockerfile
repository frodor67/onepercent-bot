FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 AIOHTTP_NO_EXTENSIONS=1

RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && apt-get autoremove -y

WORKDIR /app
COPY . .

CMD ["python", "bot.py"]
