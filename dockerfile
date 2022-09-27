# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster 

WORKDIR /tmp/search-bot

COPY . /tmp/search-bot/files

RUN pip3 install -r /tmp/search-bot/files/requirements.txt   

ENTRYPOINT ["python3"]

CMD [ "/tmp/search-bot/files/search-bot.py" ] 