FROM python:3.7-slim

WORKDIR /app

COPY src/requirements.txt  /app/
RUN pip install -r requirements.txt

COPY src/*.py src/pytest.ini /app/
COPY src/templates/*.html /app/templates/

CMD ["python", "app.py"]
