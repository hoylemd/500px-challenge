FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt dl_mock.py server.py /app/
RUN mkdir /app/cache

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
