FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5849303267:AAGsWTAQNpEH9WtwoTe8-E_J9ERI-N-aaT8"
ENV TELEGRAM_ACCESS_ID="581756128"


ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]

