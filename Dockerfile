FROM python:3.7.0

RUN mkdir /bot

WORKDIR /bot

add . /bot

RUN pip install -r requeriments.txt

CMD python main.py
