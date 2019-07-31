FROM python:3.7-slim

WORKDIR /app

COPY src/app.py src/requirements.txt src/tests.py src/utils.py src/pytest.ini /app/
COPY src/templates/index.html src/templates/detail.html /app/templates/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
