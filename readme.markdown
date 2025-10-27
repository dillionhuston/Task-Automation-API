# Task Automation API  

**Task Automation API** is a robust backend built with **FastAPI**, **Celery**, **SQLAlchemy**, and **Redis**. It empowers users to register, authenticate, and schedule automated tasks like **file cleanup** and **email reminders** at specified future times.


- **File cleanup:** Deletes files older than a configurable threshold from the `uploads/` folder.  
- **Reminders:** Sends scheduled emails to specified recipients.  
- Tested on Windows with the Celery `solo` pool for compatibility.

---
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

## Polling Server

- Run using > ```python python -m app.CLIENT.client_poll_server```
- Example output
```json
- {
  "id": "27a6884f-4fdf-459e-aaab-f85b6ceb6282",
  "user_id": "6178d57a-3881-4c68-ac3e-804636e598f6",
  "task_type": "file_cleanup",
  "schedule_time": "2025-10-27T13:19:00",
  "status": "completed",
  "title": "Clean uploads/"
}
```
-Client will delete files older than 7 days. Folder path has to be provided in 'constants.py

---

## Features & Code Quality

- Fully **PEP8-compliant** with `black` formatting and `pylint` linting  
- Strong typing enforced with Pydantic schemas and Python type hints  
- Modular architecture separating routers, services, tasks, and utilities  
- Comprehensive exception handling with meaningful error responses  
- Thread-safe singleton logger using lazy formatting and rotation  
- CI/CD friendly for GitHub Actions workflows (lint, format, test)

---

## Prerequisites

- Python 3.8+  
- Redis (Windows users: [Microsoft Redis archive](https://github.com/microsoftarchive/redis))  
- Git & virtualenv

---

## Quick Start

```bash
git clone https://github.com/dillionhuston/Task-Automation-API.git
cd Task-Automation-API

python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

redis-server  # Start Redis server

uvicorn main:app --reload  # Launch FastAPI server

celery -A worker worker --pool=solo --loglevel=info  # Start Celery worker
```

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
│ ├── init.py
│ ├── config.py # Centralized configuration loader (.env, constants)
│ ├── auth/ # JWT authentication logic
│ ├── dependencies/ # Database and shared dependencies
│ ├── models/ # SQLAlchemy models & database setup
│ ├── routers/ # FastAPI route handlers
│ ├── schemas/ # Pydantic schemas and enums
│ ├── scripts/ # Optional scripts or utilities
│ ├── tasks/ # Celery background task definitions
│ └── utils/ # Utility modules (logger, email, file ops)
│
├── CLIENT/ # Command-line client interface
│ └── client.py
│
├── uploads/ # Target folder for file cleanup
├── venv/ # Virtual environment (ignored by Git)
│
├── .env # Environment variables (email credentials)
├── .env_example # Example environment configuration
├── dev.db # Development SQLite database
├── docker-compose.yml # Docker Compose setup
├── Dockerfile # Docker build file
├── initdb.py # Database initialization script
├── main.py # FastAPI entry point
├── requirements.txt # Python dependencies
└── worker.py # Celery worker launcher
```
## Testing

This project uses pytest for testing API endpoints and Celery tasks.

### Running Tests

1. Ensure your virtual environment is activated.
2. Install test dependencies (if any additional required, else pytest is in your main deps).
3. Run tests with:

```bash
pytest
```

### Test Coverage

- Tests cover key API endpoints: registration, login, scheduling, listing, and cancellation.
- Celery task executions (file cleanup and reminders) are tested.
- Use `pytest -v` for verbose output or integrate with coverage tools for detailed reports.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions, please open an issue on the GitHub repository.
