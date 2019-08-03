FROM python:3.7-slim

WORKDIR /app

COPY dl_mock.py server.py /app
RUN mkdir /app/cache

RUN pip install -r requirements.txt

RUN python dl_mock.py

CMD ["python", "server.py"]
