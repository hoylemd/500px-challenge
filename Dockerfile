FROM python:3.7-slim

WORKDIR /app

COPY src/app.py src/requirements.txt /app/
COPY src/templates/index.html /app/templates/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
