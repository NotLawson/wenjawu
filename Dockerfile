FROM python:3.11

WORKDIR /usr/bot
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD python3 bot.py