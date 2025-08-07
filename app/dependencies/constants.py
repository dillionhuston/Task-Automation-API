"""Constants used across the application."""

from datetime import datetime, timezone
import uuid




# ========== TASK STATUS ==========
TASK_STATUS_SCHEDULED = "scheduled"
TASK_STATUS_CANCELLED = "cancelled"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"
TASK_STATUS_RUNNING= "R"

# ========== TASK TYPES ==========
TASK_TYPE_REMINDER = "reminder"
TASK_TYPE_FILE_CLEANUP = "file_cleanup"

# ========== FIELD DEFAULTS ==========
def taskscheduledefault():
    """returns uth time"""
    return datetime.now(timezone.utc)

TASK_ID_GENERATOR = uuid.uuid4

DEFAULT_TASK_TITLE = "untitled task"

# ========== JSON KEYS ==========
JSON_USER_ID = "user_id"
JSON_USER_NAME = "user_name"
JSON_TASK_ID = "task_id"
JSON_STATUS = "status"

# ========== HTTP STATUS CODES ==========
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_NOT_APPLICABLE = 406
HTTP_STATUS_SERVER_ERROR = 500


# ========== FILE STORAGE ==========
FILE_STORAGE_DIR = "./uploads"
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_FILE_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
