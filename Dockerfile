FROM python:3.7-slim

WORKDIR /app

COPY src/requirements.txt src/*.py src/pytest.ini /app/
COPY src/templates/*.html /app/templates/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
