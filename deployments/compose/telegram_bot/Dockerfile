FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=core.settings

ENV PYTHONPATH=/app

CMD ["python", "apps/infobot/InfoBot/main.py"]