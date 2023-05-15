FROM python:alpine

# Change your time zone here accordingly (for logging)
ENV TZ=Asia/Singapore

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app/spinnit

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
# `your telegram token` -> '<your token from BotFather>'
ENV TELEGRAM_TOKEN='your telegram token'

# `your developer chat id` -> 'Your Telegram ID (you can use this bot _@userinfobot_ to get your Telegram ID)
ENV DEVELOPER_CHAT_ID='your developer chat id'

# `your special ids` -> `'<Telegram IDs that can use the special mode>'` (separated by spaces e.g. '123456789 987654321')
# If you only want yourself to be a special user, you can leave this unchanged.
# Note: Special mode i.e. see special pictures for special users requires you to provide
# square pictures in the form of .png/.jpg/.jpeg (unless you want stretched pictures) in the special folder
# (under `assets/images`), Spinnit! will use the general pictures if special pictures cannot be found.
# Regardless of special pictures, special users will have the increased cap of 10 /spin commands
# every 5 minutes instead of 2.
ENV SPECIAL_IDS='your special ids'

WORKDIR /app/spinnit/src/main

CMD [ "python", "main.py" ]

# docker build -t spinnit:latest .
# docker run -d -v spinnit:/app/spinnit/logs --name spinnit spinnit