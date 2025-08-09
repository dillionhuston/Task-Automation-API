# Task Automation API

Hi all,

This repository is a task-automation backend built with **FastAPI**, **Celery**, **SQLAlchemy**, and **Redis**. It allows users to register, log in, and schedule two types of tasks—**file cleanup** or **reminders**—at future times. File cleanup removes files older than a configurable age from the `uploads/` folder, and reminders send emails to a specified address. The project is asynchronous, tested on Windows with the solo Celery pool, and serves as a portfolio project showcasing real-world backend skills.

## Why This Project
This project demonstrates:
- **FastAPI**’s dependency injection and Pydantic models  
- **Celery** for background job processing  
- **SQLAlchemy** for database access  
- A production-ready rotating-file logger setup  
- Solutions for Windows-specific Celery issues ([WinError 6])  
- Clean code practices: type hints, enums, and consistent status codes  

## Best Practices & Code Quality
- **PEP8–compliant**: Code formatted with `black` and linted by `pylint`.  
- **Strict typing**: Full use of Pydantic schemas and Python type hints.  
- **Modular architecture**: Separation of concerns across routers, services, tasks, and utilities.  
- **Exception handling**: Clear, specific error responses and chained exceptions (`raise … from`).  
- **Logging**: Thread-safe singleton logger, lazy formatting (`%s`), and rotating file support.  
- **CI/CD ready**: Easy integration with GitHub Actions for linting, formatting, and tests.  

## Prerequisites
- **Python 3.8+**
- **Redis** (on Windows, use [Microsoft’s Redis archive](https://github.com/microsoftarchive/redis))
- **Git** and a **virtualenv**

## Setup
1. **Clone & Navigate**
   ```bash
   git clone https://github.com/dillionhuston/Task-Automation-API.git
   cd Task-Automation-API
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv .venv
   .\venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
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

## Usage
- Access interactive API docs at `http://localhost:8000/docs`
- **Register** a user (`POST /register`), then **log in** (`POST /login`) to obtain a Bearer token
- **Schedule tasks** (`POST /schedule`) with the following fields:
  - `task_type`: `"file_cleanup"` or `"reminder"`
  - `schedule_time`: ISO UTC datetime (must be in the future)
  - `receiver_email`: Required for reminders
- **List tasks** (`GET /list_tasks`) and **cancel tasks** (`GET /cancel/{task_id}`)
- **File cleanup**: Deletes files older than 7 days in `uploads/` by default

### Email Reminders
Add a `.env` file with:
```bash
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
```
- Enable 2FA on your Gmail account and create an [app password](https://support.google.com/accounts/answer/185833).
- Include `receiver_email` when scheduling reminder tasks.

**Sample Payload:**
```json
{
  "task_type": "reminder",
  "schedule_time": "2025-08-10T14:00:00Z",
  "receiver_email": "user@example.com"
}
```

Task-Automation-API/
├── app/
│   ├── auth/          # JWT login/refresh routes
│   ├── dependencies/  # Dependency injection logic
│   ├── models/        # SQLAlchemy database models
│   ├── routers/       # File, task, and auth endpoints
│   ├── schemas/       # Pydantic models & enums
│   ├── scripts/       # Utility scripts
│   ├── tasks/         # Celery task implementations
│   └── utils/         # Logger, email, hashing, Celery setup
├── .env               # Environment variables
├── .gitignore         # Git ignore file
├── initdb.py          # Database initialization script
├── main.py            # FastAPI application entry point
├── README.md          # Project documentation
├── reminder_email.png # Sample reminder email image
├── requirements.txt   # Project dependencies
├── task_automation.db # SQLite database
└── worker.py          # Celery worker configuration
```

## Next Steps
- Write **pytest** suites for endpoints and tasks
- Dockerize with **Docker Compose** for easy deployment
- Make available on public network 

Feel free to clone, explore, and open issues or PRs. Thanks for checking it out!
