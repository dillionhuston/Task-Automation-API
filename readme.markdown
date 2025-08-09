# Task Automation API

This repository is a task-automation backend built with **FastAPI**, **Celery**, **SQLAlchemy**, and **Redis**. It allows users to register, log in, and schedule two types of tasks—**file cleanup** or **reminders**—at future times.

- **File cleanup** removes files older than a configurable age from the `uploads/` folder  
- **Reminders** send emails to a specified address  
- Tested on Windows with the solo Celery pool  

---

## Why This Project

- **FastAPI**’s dependency injection and Pydantic models  
- **Celery** for background job processing  
- **SQLAlchemy** for database access  
- Production-ready rotating-file logger setup  
- Solutions for Windows-specific Celery issues ([WinError 6])  
- Clean code practices: type hints, enums, and consistent status codes  

---

## Best Practices & Code Quality

- **PEP8-compliant**: Formatted with `black` and linted by `pylint`  
- **Strict typing**: Full Pydantic schemas and Python type hints  
- **Modular architecture**: Clear separation across routers, services, tasks, and utilities  
- **Exception handling**: Specific error responses and chained exceptions (`raise … from`)  
- **Logging**: Thread-safe singleton logger, lazy formatting (`%s`), and rotating file support  
- **CI/CD ready**: Easy integration with GitHub Actions for linting, formatting, and tests  

---

## Prerequisites

- **Python 3.8+**  
- **Redis** (on Windows, use [Microsoft’s Redis archive](https://github.com/microsoftarchive/redis))  
- **Git** and a **virtualenv**  

---

## Setup

1. **Clone & Navigate**  
   ```bash
   git clone https://github.com/dillionhuston/Task-Automation-API.git
   cd Task-Automation-API
   ```

2. **Create & Activate Virtualenv**  
   ```bash
   python -m venv .venv
   .\venv\Scripts\activate     # Windows
   source .venv/bin/activate    # macOS/Linux
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis**  
   ```bash
   redis-server
   ```

5. **Run FastAPI**  
   ```bash
   uvicorn main:app --reload
   ```

6. **Start Celery Worker**  
   ```bash
   celery -A app.utils.celery_instance.celery_app worker --pool=solo --loglevel=info
   ```

---

## Usage

- **Docs**: `http://localhost:8000/docs`  
- **Register**: `POST /register`  
- **Login**: `POST /login` → Bearer token  
- **Schedule Task**: `POST /schedule`  
  ```json
  {
    "task_type": "file_cleanup" | "reminder",
    "schedule_time": "2025-08-10T14:00:00Z",
    "receiver_email": "user@example.com"  # required for reminders
  }
  ```
- **List Tasks**: `GET /list_tasks`  
- **Cancel Task**: `GET /cancel/{task_id}`  
- **File cleanup**: Deletes files older than 7 days in `uploads/` by default  

---

## Email Reminders

Add a `.env` file:
\`\`\`bash
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
\`\`\`
- Enable 2FA on Gmail and create an [app password](https://support.google.com/accounts/answer/185833).  
- Include \`receiver_email\` when scheduling reminder tasks.  

---
# PROJECT STRUCTURE

Task-Automation-API/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth/                # JWT login/refresh routes
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── routers/             # All FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── files.py
│   │   └── tasks.py
│   ├── schemas/             # Pydantic models & enums
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── models/              # SQLAlchemy models & DB
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── file.py
│   │   └── task.py
│   ├── dependencies/        # DI & constants
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── constants.py
│   ├── tasks/               # Celery task implementations
│   │   ├── __init__.py
│   │   └── cleanup.py
│   ├── utils/               # Helpers: logger, email, file‐ops
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── email.py
│   │   └── file_ops.py
│   └── celery_app.py        # Celery instance (instead of utils/__init__)
├── uploads/                 # Where file‐cleanup runs
├── .env
├── .gitignore
├── initdb.py
├── requirements.txt
├── task_automation.db
└── worker.py


## Next Steps

- Write **pytest** suites for endpoints and tasks  
- Dockerize with **Docker Compose** for easy deployment  
- Integrate **GitHub Actions** for automated linting, formatting, and testing  
- Publish as a **Docker image** or **PyPI package**  

Feel free to clone, explore, and open issues or PRs. Thanks for checking it out!
