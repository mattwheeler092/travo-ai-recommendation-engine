FROM python:3.9-slim

RUN mkdir /app
RUN mkdir /app/data

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/. .
COPY .env .

CMD ["uvicorn", "server:app", "--host=0.0.0.0", "--port=80"]