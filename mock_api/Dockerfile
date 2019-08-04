FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY dl_mock.py server.py /app/
RUN mkdir /app/cache

CMD ["python", "server.py"]
