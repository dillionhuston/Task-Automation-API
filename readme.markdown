
# Task Automation API Platform

## Overview
The Task Automation API Platform is a backend-only FastAPI application that enables users to upload files, schedule automated tasks (e.g., reminders, cleanup jobs), and receive email notifications. It features secure JWT-based authentication, admin tools, and containerized deployment with Docker. This project showcases skills in building scalable, secure APIs with modern Python technologies.

## Features
- User Authentication: Secure registration and login with JWT.
- File Management: Upload, list, and delete files with SHA-256 hash validation.
- Task Scheduler: Schedule and manage background tasks (reminders, file cleanup).
- Background Processing: Asynchronous task execution with Celery.
- Email Notifications: Alerts for task events (creation, completion, failure).
- Admin Tools: CLI and API for user/task management.
- Deployment: Containerized with Docker and Docker Compose.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (production), SQLite (development)
- **ORM**: SQLAlchemy with Alembic
- **Task Queue**: Celery with Redis
- **Email**: SendGrid or smtplib
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, FastAPI TestClient
- **Security**: python-jose (JWT), passlib
- **Other**: python-multipart, python-dotenv

## Project Structure
```
task_automation_api/
├── app/
│   ├── main.py           # FastAPI app
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication logic
│   ├── routes/           # API endpoints
│   │   ├── users.py
│   │   ├── files.py
│   │   ├── tasks.py
│   │   └── admin.py
│   ├── tasks.py          # Celery tasks
│   ├── utils/            # Helpers
│   │   ├── email.py
│   │   ├── file.py
│   │   └── task.py
│   ├── dependencies.py   # Dependency injection
│   └── config.py         # Configuration
├── migrations/           # Alembic migrations
├── tests/                # Tests
│   ├── test_auth.py
│   ├── test_files.py
│   ├── test_tasks.py
│   └── test_admin.py
├── scripts/              # Admin CLI
│   └── admin_cli.py
├── .env                  # Environment variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pytest.ini
```

## Timeline (8 Weeks)
- **Week 1**: Project setup, user authentication.
- **Week 2**: File management system.
- **Week 3**: Task scheduling system.
- **Week 4**: Celery background processing.
- **Week 5**: Email notifications.
- **Week 6**: Admin tools.
- **Week 7**: Testing and polish.
- **Week 8**: Deployment and documentation.

## Milestones
1. Week 1: User registration/login with JWT.
2. Week 2: File upload/list/delete with hash validation.
3. Week 3: Task scheduling in database.
4. Week 4: Celery tasks with Docker Compose.
5. Week 5: Email notifications.
6. Week 6: Admin CLI/API.
7. Week 7: 80%+ test coverage, Swagger UI.
8. Week 8: Production-ready deployment.

## Notes for Coding
- Use `.env` for secrets (include `.env.example`).
- Start with SQLite, switch to PostgreSQL in Week 4.
- Write tests alongside features.
- Validate inputs, secure JWTs, sanitize uploads.
- Optimize database queries with indexes.
- Update README weekly.

## Next Steps
1. Set up Git repository and commit initial skeleton.
2. Follow Week 1 tasks for authentication.
3. Review progress weekly against milestones.
