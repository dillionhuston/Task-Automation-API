# Task Automation API
![Banner](assets/home.png)
[![Build Status](https://img.shields.io/github/actions/workflow/status/dillionhuston/Task-Automation-API/ci.yml)](https://github.com/dillionhuston/Task-Automation-API/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

**A production-ready, modular backend service for scheduling and automating recurring tasks** — including **automatic file cleanup**, **email reminders**, and **task history tracking**.
---

Built with **FastAPI**, **Celery**, **Redis**, and **SQLAlchemy**, featuring secure JWT authentication, background task processing, and webhook notifications.


##  Features

- **Automated File Cleanup** – Delete old files from local directories on a schedule(locally)
- **Email Reminders** – Send timed email notifications with full content customization  
- **Secure Authentication** – JWT-based login/register with protected routes  
- **Background Task Execution** – Powered by Celery + Redis for reliable scheduling  
- **Webhook Notifications** – Get real-time updates when tasks complete or fail  
- **Rich CLI Client** – Full-featured terminal interface for task management  
- **Task History & Cancellation** – List, monitor, and cancel scheduled tasks  
![Task List & History](assets/tasks.png)
- **Modular & Type-Safe** – Clean architecture with Pydantic validation and full typing  
- **Production-Ready Logging** – Thread-safe singleton logger with structured output  
- **Docker Compose Deployment** – One-command full-stack deployment  
- **100% PEP8 Compliant** – Formatted with Ruff/Black, tested and linted

---
![Email reminder dmemo](assets/addtask.png)



##  Quickstart (Dev)
```bash
git clone https://github.com/dillionhuston/Task-Automation-API.git
cd Task-Automation-API

python -m venv venv ** source .venv/bin/activate
pip install -r requirements.txt
```

## Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Launch FastAPI (with auto reload)
uvicorn main:app --reload

# Terminal 3: Start Celery Worker
celery -A worker worker --pool=solo --loglevel=info

# Terminal 4: Run CLI Client
python -m app.CLIENT.client_poll_server
```


## Using the CLI Client
## CLI client is located at `app/CLIENT/client.py`

# 1. Signup
python app/CLIENT/client.py signup --email john@example.com --password pass12334 --username john

# 2. Login
python app/CLIENT/client.py login --email john@example.com --password pass12334

# 3. Create File Cleanup Task
python app/CLIENT/client.py create_task \
  --task_type file_cleanup \
  --schedule_time "Oct 27 1:04pm" \
  --title "Clean uploads/"

# 4. Schedule an Email Reminder
python app/CLIENT/client.py create_task \
  --task_type reminder \
  --schedule_time "Oct 28 7pm" \
  --receiver_email "john@example.com" \
  --title "Team Standup"

![reminde demo](assets/example_task.png)


---

# API Endpoints (Swagger UI)
## Once running: http://localhost:8000/docs

| Method   | Endpoint              | Description                  |
|----------|-----------------------|------------------------------|
| `POST`   | `/register`           | Create a new user account    |
| `POST`   | `/login`              | Authenticate and get JWT token |
| `POST`   | `/schedule`           | Schedule a new task          |
| `GET`    | `/list_tasks`         | View all scheduled tasks     |
| `DELETE` | `/cancel/{task_id}`   | Cancel a pending task        |
| 'GET'    | '/tasks/task_history' | Gets task history of user    |



## Email Setup (.env)
Create a `.env` file with your Gmail credentials:

```bash
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///./dev.db
JWT_SECRET=your-super-secret-jwt-key-here
```

**Gmail Users:** Enable 2FA and create an **App Password** for secure email sending.  
You can also refer to the included `.env_example` file for a template of all required environment variables.


# Production deployment (Docker Compose)

```bash 
docker compose up --build
docker-compose up
```
**Make sure to have docker or docker desktop installed on your system**

This starts:
- FastAPI(port 8000)
- Celery Worker
- Redis
- Postgre-SQL ready config, Just switch DATABASE_URL. In .env
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
|   ├── scripts/         # Admin client script
│   ├── tasks/           # Celery task definitions
│   └── utils/           # Logger, email, helpers
|   └── config.py        # Config file
├── main.py              # FastAPI entry point
├── worker.py            # Celery worker launcher
├── Dockerfile           # Multi-stage production image         
├── initdb.py            # Create Database 

├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build file
├── docker-compose.yml   # Docker Compose setup
└── dev.db               # SQLite development DB, PostgreSQL available for prod
  ```
# Contributing

## Contributions are very welcome! Here's how:

### How to Contribute

1. **Fork** the repository.  

2. **Create a branch** for your feature or bugfix:  ``` git checkout -b feature/my-feature```

3. Make your changes and commit with a clear message:```git commit -m "Add feature X"```

4. Push your branch to your fork: ```git push origin feature/my-feature```

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

