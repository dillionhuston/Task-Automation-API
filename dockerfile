FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
