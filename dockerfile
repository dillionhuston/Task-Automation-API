FROM python:3.10-slim

# Install SQLite shared libraries
RUN apt-get update && apt-get install -y libsqlite3-0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expose port 8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
