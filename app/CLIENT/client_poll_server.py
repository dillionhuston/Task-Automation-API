import time
import requests
from datetime import datetime
from app.tasks.tasks import file_cleanup
from app.dependencies.constants import TASK_STATUS_SCHEDULED
from app.models.database import SessionLocal
from app.models.tasks import TaskHistory

HOST = "http://localhost:8000"
TOKEN_FILE = r"C:\Users\amazo\Desktop\Projects\Network_monitor\Task-Automation-API\Task-Automation-API\app\CLIENT\token.txt"
POLL_INTERVAL = 10  # seconds


def load_token(token_path: str) -> str | None:
    """Load API token from file."""
    try:
        with open(token_path) as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] Token file not found: {token_path}")
        return None


def show_task_history(limit: int = 5):
    """Display the last N executed tasks from TaskHistory."""
    with SessionLocal() as db:
        histories = (
            db.query(TaskHistory)
            .order_by(TaskHistory.executed_at.desc())
            .limit(limit)
            .all()
        )
        if histories:
            print("\n--- Task History (Last {} Executions) ---".format(limit))
            print(f"{'Task Type':<15} {'Status':<10} {'Executed At':<20} {'Details'}")
            for h in histories:
                executed = h.executed_at.strftime("%Y-%m-%d %H:%M")
                print(f"{h.task_type:<15} {h.status:<10} {executed:<20} {h.details}")


def poll_server():
    """Main loop to poll the server for tasks and execute them on schedule."""
    token = load_token(TOKEN_FILE)
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    print("[INFO] Starting task polling loop...")

    while True:
        try:
            response = requests.get(f"{HOST}/list_tasks", headers=headers)
            if response.status_code != 200:
                print(f"[ERROR] Server returned {response.status_code}: {response.text}")
                time.sleep(POLL_INTERVAL)
                continue

            tasks = response.json()
            if not tasks:
                print("[INFO] No tasks available.")
                time.sleep(POLL_INTERVAL)
                continue

            print("\n--- Retrieved Tasks ---")
            for task in tasks:
                task_id = task.get("id")
                task_type = task.get("task_type")
                status = task.get("status")
                receiver_email = task.get("receiver_email")
                schedule_time_str = task.get("schedule_time")

                print(f"→ ID {task_id} | Type {task_type} | Status {status}")

                # Only run file_cleanup tasks that are scheduled
                if task_type != "file_cleanup" or status not in (TASK_STATUS_SCHEDULED,):
                    continue

                if not schedule_time_str:
                    print(f"[WARN] Task {task_id} has no schedule_time set.")
                    continue

                schedule_time = datetime.fromisoformat(schedule_time_str)
                now = datetime.now()

                if now >= schedule_time:
                    print(f"[EXECUTE] Running task {task_id}")
                    try:
                        file_cleanup(task_id, receiver_email)
                    except Exception as e:
                        print(f"[ERROR] Failed to execute task {task_id}: {e}")
                else:
                    time_left = (schedule_time - now).total_seconds()
                    print(f"[WAIT] Task {task_id} runs in {int(time_left)}s")

            # Display last 5 task history entries
            show_task_history(limit=5)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection issue: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    poll_server()
