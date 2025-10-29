import time
import requests
from datetime import datetime
from app.tasks.tasks import file_cleanup
from app.dependencies.constants import  TASK_STATUS_SCHEDULED

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

                # Only run file_cleanup tasks that are pending or scheduled
                if task_type != "file_cleanup" or status not in ( TASK_STATUS_SCHEDULED):
                    continue

                if not schedule_time_str:
                    print(f"[WARN] Task {task_id} has no schedule_time set.")
                    continue

                schedule_time = datetime.fromisoformat(schedule_time_str)
                now = datetime.now()

                if now >= schedule_time:
                    print(f"[EXECUTE] Running task {task_id}")
                    try:
                        # Run cleanup and send email via Celery
                        file_cleanup(task_id, receiver_email)
        
                    except Exception as e:
                        print(f"[ERROR] Failed to execute task {task_id}: {e}")
                        # Update server to failed status
                        try:
                            requests.put(
                                f"{HOST}/update_task_status/{task_id}",
                                json={"status": "failed"},
                                headers=headers
                            )
                        except Exception as update_err:
                            print(f"[ERROR] Failed to update task status for {task_id}: {update_err}")
                else:
                    time_left = (schedule_time - now).total_seconds()
                    print(f"[WAIT] Task {task_id} runs in {int(time_left)}s")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection issue: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    poll_server()
