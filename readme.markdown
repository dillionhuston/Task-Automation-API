# Task Automation API

A FastAPI-based task scheduler for users to register, log in, and schedule tasks (`file_cleanup` or `reminder`) to run at future times. The `file_cleanup` task deletes files older than 7 days in the `uploads` directory. Built with Celery for asynchronous tasks, SQLAlchemy for database management, and Redis as the broker/backend, this project showcases backend development and Windows debugging skills for a portfolio.

## Why This Project
This API demonstrates my ability to build a scalable backend with FastAPI, Celery, and SQLAlchemy, while solving real-world problems like file cleanup. I debugged Windows-specific Celery issues (`[WinError 6]`) using the `solo` pool, reinforcing my problem-solving skills for a backend developer role.

## Prerequisites
- Python 3.8+
- Redis - Download from [Microsoft Redis Archive](https://github.com/microsoftarchive/redis/releases) for Windows
- Virtual environment
- Packages: `fastapi`, `uvicorn`, `celery`, `redis`, `sqlalchemy`, `pydantic`

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Task-Automation-API
   ```

2. **Activate Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows; use `source venv/bin/activate` for Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn celery redis sqlalchemy pydantic
   ```

4. **Start Redis**
   ```bash
   redis-server
   ```
   Verify with `redis-cli ping` (should return `PONG`).

5. **Run FastAPI**
   ```bash
   fastapi dev main.py
   ```
   Access at `http://localhost:8000`. Use `http://localhost:8000/docs` for interactive API docs. Check health:
   ```bash
   curl http://localhost:8000/health
   ```
   Expected output: `{"success": 200}`

6. **Start Celery Worker**
   ```bash
   celery -A app.utils.celery_instance.celery_app worker --pool=solo --loglevel=info
   ```
   Ensures Windows compatibility.

## Usage

Use `http://localhost:8000/docs` for most interactions (recommended). Alternatively, use `curl`.

1. **Register**
   - **Docs**: In `/docs`, use `/register` (POST) with `username` and `password`.
   - **curl**:
     ```bash
     curl -X POST "http://localhost:8000/register" -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
     ```

2. **Log In**
   - **Docs**: Use `/login` (POST) to get a token.
   - **curl**:
     ```bash
     curl -X POST "http://localhost:8000/login" -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
     ```

3. **Schedule a Task**
   Schedule `file_cleanup` (deletes files older than 7 days in `uploads`) or `reminder` for a future time (UTC, e.g., `2025-08-02T20:00:00Z` for 8:00 PM UTC, after 7:36 PM BST, August 2, 2025).
   - **Docs**: Use `/schedule` (POST), select `task_type` (`file_cleanup` or `reminder`), set `schedule_time`, and authorize with token.
   - **curl**:
     ```bash
     curl -X POST "http://localhost:8000/schedule" -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"task_type": "file_cleanup", "schedule_time": "2025-08-02T20:00:00Z"}'
     ```
   - Ensure `uploads` exists with test files for `file_cleanup`.
   - **Expected Celery Log**:
     ```
     Task app.tasks.tasks.file_cleanup[41bf67a4-8cf3-4b35-9eaf-6d9f4dc5b178] received
     ```

4. **List/Cancel Tasks**
   - **List (Docs)**: Use `/list_tasks` (GET) with token.
   - **List (curl)**:
     ```bash
     curl -X GET "http://localhost:8000/list_tasks" -H "Authorization: Bearer <your_token>"
     ```
   - **Cancel (Docs)**: Use `/cancel/{task_id}` (GET) with token.
   - **Cancel (curl)**:
     ```bash
     curl -X GET "http://localhost:8000/cancel/<task_id>" -H "Authorization: Bearer <your_token>"
     ```


# Enabling Email Reminders for Tasks

To enable email reminders for tasks, follow these steps:

## 1. Add Your Details

Update the `.env` file with your Gmail address and app password. Example:
```bash
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```


## 2. Create an App Password in Google

Since Gmail requires app passwords for third-party apps:

- Go to your [Google Account settings](https://myaccount.google.com/).
- Enable 2-factor authentication if not already enabled.
- Navigate to **Security > App passwords**.
- Generate an app password and use that 16-digit password in the `.env` file.

## 3. Example Reminder

See the image below for a sample email reminder sent by the system:

![Email Reminder Example](reminder_email.png)

## 4. Specify Receiver Email

When scheduling a reminder task, make sure to include the receiver_email in the request payload. For example:
```json
{
  "task_type": "file_cleanup",
  "schedule_time": "2025-08-04T18:02:11.070Z",
  "title": "hello",
  "receiver_email": "user@example.com"
}
```

   

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

## Notes
- **FastAPI Docs**: Use `http://localhost:8000/docs` for easy testing; `curl` is an alternative.
- **Tasks**:
  - `file_cleanup`: Deletes files in `uploads` older than 7 days, can be changed.
  - `reminder`: Assumed for notifications (define in `app/tasks/tasks.py`).
- **Scheduling**: `schedule_time` must be future-dated (UTC).
- **Windows**: `--pool=solo` avoids `[WinError 6]` errors.
- **Portfolio**: Showcases FastAPI, Celery, SQLAlchemy, and debugging skills.


## Future Improvements
- Validate future `schedule_time`.
- Implement `reminder` (e.g., email notifications).
- Add Celery Beat for recurring tasks.
- Deploy to Render.com.
