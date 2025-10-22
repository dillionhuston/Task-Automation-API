# Task Automation API

**Task Automation API** is a robust backend built with **FastAPI**, **Celery**, **SQLAlchemy**, and **Redis**. It empowers users to register, authenticate, and schedule automated tasks like **file cleanup** and **email reminders** at specified future times.

- **File cleanup:** Deletes files older than a configurable threshold from the `uploads/` folder.  
- **Reminders:** Sends scheduled emails to specified recipients.  
- Tested on Windows with the Celery `solo` pool for compatibility.

---

## Why Choose This Project?

- Built with **FastAPI** leveraging dependency injection and Pydantic for data validation  
- Asynchronous background task execution with **Celery** and **Redis**  
- Robust database layer via **SQLAlchemy** ORM  
- Production-ready logging with rotating file handlers  
- Windows-specific Celery issue workarounds (e.g., [WinError 6])  
- Clean, maintainable code using type hints, enums, and consistent HTTP status codes  

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

uvicorn app.main:app --reload  # Launch FastAPI server

celery -A app.celery_app.celery_app worker --pool=solo --loglevel=info  # Start Celery worker
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
```

**Note:** Enable 2FA and create an app password for secure email sending.

## Project Structure

```
Task-Automation-API/
├── app/
│   ├── models/         # Database models
│   ├── routers/       # API endpoints
│   ├── schemas/       # Pydantic schemas
│   ├── tasks/         # Celery tasks (file_cleanup)
│   ├── utils/         # Celery and scheduling logic
│   ├── main.py        # FastAPI entry point
├── uploads/           # Files for file_cleanup (deletes files >7 days old)
├── venv/             # Virtual environment
├── README.md         # This file
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
