FROM python:3.7-slim

WORKDIR /app

COPY app.py requirements.txt /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
