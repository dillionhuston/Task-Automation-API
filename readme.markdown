# Task Automation API
![Banner](assets/home.png)
**[Try the Live Demo](https://dillonhtask.netlify.app/)**

[![Build Status](https://img.shields.io/github/actions/workflow/status/dillionhuston/Task-Automation-API/ci.yml)](https://github.com/dillionhuston/Task-Automation-API/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

**A production ready, modular backend service for scheduling and automating recurring tasks** — including **Secure file storage system**, **email reminders**, and **task history tracking**.

---

Built with **FastAPI**, **Celery**, **Redis**, and **SQLAlchemy**, featuring secure JWT authentication, background task processing, and webhook notifications.

**Frontend not included. See live demo for more**

---

## Tech Stack

### Backend Framework
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Database & ORM
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

### Task Queue & Caching
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

### Security & Validation
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

### DevOps & Deployment
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Code Quality
![Ruff](https://img.shields.io/badge/Ruff-261230?style=for-the-badge&logo=ruff&logoColor=white)
![Black](https://img.shields.io/badge/Black-000000?style=for-the-badge&logo=python&logoColor=white)

---

##  Features (v1.0)

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

##  New Features & Technical Updates (v2.0)

This update introduces major improvements to the Task Automation API, focusing on **enhanced file handling**, **dashboard capabilities**, and **task scheduling with file support**.

### New Features

- **Custom File Hashing & Validation** – Self made security system for verifying file integrity and preventing tampering  
- **Secure File Uploading & Storage** – Government grade file handling with encryption, validation, and secure storage mechanisms  
- **File Attachments in Email Reminders** – Tasks can now include file attachments that are securely processed and delivered via email  
- **File Decryption via Celery** – Files are securely decrypted in the background before being sent via email, ensuring the server never sees plaintext data  
- **Combined Dashboard View** – View all tasks and uploaded files on a single page for easy monitoring and management  
- **Task Reminder Email** – Automatic email notifications are sent when a task is due, including attached files if applicable  
- **Backend Cleanup & Linting** – Full codebase checked with Ruff, type-safe Pydantic models, and structured logging improvements  

### Technical Improvements

- **Custom Security Layer** – Built from scratch file hashing algorithms and validation routines for maximum security control  
- **Optimized Celery Task Workflow** – Background tasks are more robust, handle optional files, and include retry/backoff for SMTP errors  
- **Refined Email Module** – Centralized email logic with support for optional attachments, secure SMTP connections, and logging of successes/failures  
- **Database Enhancements** – Improved SQLAlchemy queries for files, tasks, and history tracking  
- **Deployment Ready** – Docker Compose setup updated for production deployment; works seamlessly with FastAPI, Redis, and PostgreSQL  

### Benefits

- Advanced codebase combining one year of development into one unified system  
- Custom built security features created for this application's needs  
- Easier task monitoring with all files/tasks in one dashboard  
- Safer and more reliable email delivery with optional encrypted file attachments  
- Scalable and maintainable architecture for future feature additions

![Email reminder demo](assets/addtask.png)

---

##Quickstart (Dev)
```bash
git clone https://github.com/dillionhuston/Task-Automation-API.git
cd Task-Automation-API

python -m venv venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Start Services
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

---

## Using the CLI Client
CLI client is located at `app/CLIENT/client.py`

```bash
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
```

![reminder demo](assets/example_task.png)

---

## API Endpoints (Swagger UI)
Once running: **http://localhost:8000/docs**

| Method   | Endpoint              | Description                  |
|----------|-----------------------|------------------------------|
| `POST`   | `/register`           | Create a new user account    |
| `POST`   | `/login`              | Authenticate and get JWT token |
| `POST`   | `/schedule`           | Schedule a new task          |
| `GET`    | `/list_tasks`         | View all scheduled tasks     |
| `DELETE` | `/cancel/{task_id}`   | Cancel a pending task        |
| `GET`    | `/tasks/task_history` | Gets task history of user    |

---

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

---

## Production Deployment (Docker Compose)

```bash 
docker compose up --build
```
**Make sure to have Docker or Docker Desktop installed on your system**

This starts:
- FastAPI (port 8000)
- Celery Worker
- Redis
- PostgreSQL ready config, just switch DATABASE_URL in .env

---

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
│   ├── scripts/         # Admin client script
│   ├── tasks/           # Celery task definitions
│   ├── utils/           # Logger, email, helpers
│   └── config.py        # Config file
├── main.py              # FastAPI entry point
├── worker.py            # Celery worker launcher
├── Dockerfile           # Multi-stage production image         
├── initdb.py            # Create Database 
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker Compose setup
└── dev.db               # SQLite development DB, PostgreSQL available for prod
```

---

## Contributing

Contributions are very welcome! Here's how:

### How to Contribute

1. **Fork** the repository  

2. **Create a branch** for your feature or bugfix:  
   ```bash
   git checkout -b feature/my-feature
   ```

3. Make your changes and commit with a clear message:  
   ```bash
   git commit -m "Add feature X"
   ```

4. Push your branch to your fork:  
   ```bash
   git push origin feature/my-feature
   ```

5. **Open a Pull Request** and describe your changes

---

## License
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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.