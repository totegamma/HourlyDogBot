FROM python:3

COPY src/main.py ./

RUN pip3 install websockets misskey.py

CMD ["python3", "main.py"]

