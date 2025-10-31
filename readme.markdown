# Task Automation API
[![Build Status](https://img.shields.io/github/actions/workflow/status/dillionhuston/Task-Automation-API/ci.yml)](https://github.com/dillionhuston/Task-Automation-API/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

**A powerful, modular backend service for scheduling and executing automated tasks** — including **file cleanup** and **email reminders** — built with **FastAPI**, **Celery**, **SQLAlchemy**, and **Redis**.

---

##  Features

- **File Cleanup Tasks** — Automatically delete old files from specified directories  
- **Email Reminders** — Schedule and send email notifications at precise times  
- **JWT-based Authentication** — Secure `register` and `login` endpoints  
- **Modular Architecture** — Clean separation: routers, services, tasks, utils  
- **Thread-Safe Singleton Logger** — Lazy formatting, production-ready logging  
- **Strong Typing & Validation** — Full Pydantic schema enforcement  
- **CLI Client** — Interact with the API directly from the terminal  
- **100% PEP8 Compliant** — Linted, formatted, and ready for production  

---

##  Quickstart
```bash
git clone https://github.com/dillionhuston/Task-Automation-API.git
cd Task-Automation-API
python -m venv .venv
pip install -r requirements.txt
```

## Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Launch FastAPI
uvicorn main:app --reload

# Terminal 3: Start Celery Worker
celery -A worker worker --pool=solo --loglevel=info

# Terminal 4: Run CLI Client
python -m app.CLIENT.client_poll_server
```

## Client Usage (CLI) Located at /CLIENT/client.py
```bash
# 1. Signup
python app/CLIENT/client.py signup --email john@example.com --password pass12334 --username john

# 2. Login
python app/CLIENT/client.py login --email john@example.com --password pass12334

# 3. Create File Cleanup Task (deletes files >7 days old in folder defined in constants.py
python app/CLIENT/client.py create_task \
  --task_type file_cleanup \
  --schedule_time "Oct 27 1:04pm" \
  --title "Clean uploads/"

# 4. Create Reminder Task
python app/CLIENT/client.py create_task \
  --task_type reminder \
  --schedule_time "Oct 28 7pm" \
  --receiver_email "john@example.com" \
  --title "Team Standup"

```
---

## API Usage
Visit Swagger UI: http://localhost:8000/docs
1. **Register**: `POST /register`
2. **Login**: `POST /login` (receive Bearer token)
3. **Schedule a task**: `POST /schedule`
```json
{
  "task_type": "file_cleanup" | "reminder",
  "schedule_time": "2025-08-10T14:00:00Z",
  "receiver_email": "user@example.com"  # Required for reminders
}
```
4. **List scheduled tasks**: `GET /list_tasks`
5. **Cancel a task**: `GET /cancel/{task_id}`

## Email Reminders Setup
Create a `.env` file with your Gmail credentials:

```bash
EMAIL=your_email@gmail.com
PASSWORD=your_app_password

**Note:** Enable 2FA and create an app password for secure email sending.  
You can also refer to the included `.env_example` file for a template of all required environment variables.
```
## Project Structure
```bash
Task-Automation-API/
├── app/
│   ├── auth/            # JWT authentication
│   ├── CLIENT/          # Command-line client interface
│   ├── dependencies/    # Shared dependencies
│   ├── models/          # SQLAlchemy models
│   ├── routers/         # FastAPI routes
│   ├── schemas/         # Pydantic schemas
│   ├── tasks/           # Celery task definitions
│   └── utils/           # Logger, email, helpers
├── uploads/             # Target folder for cleanup
├── main.py              # FastAPI entry point
├── worker.py            # Celery worker launcher
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build file
├── docker-compose.yml   # Docker Compose setup
└── dev.db               # SQLite development DB
```

## Production Deployment with Docker Compose
Deploy the full stack (FastAPI + Celery + Redis) using Docker Compose.
## Run 
```bash
docker-compose up --build -d
```
##  License

MIT License

Copyright (c) 2025 Dillion Huston

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

