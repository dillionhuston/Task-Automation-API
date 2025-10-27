import time
import requests

from app.tasks.tasks import file_cleanup

host = "http://localhost:8000"



def poll_server(interval=10):
    try:
        with open(r"C:\Users\amazo\Desktop\Projects\Network_monitor\Task-Automation-API\Task-Automation-API\app\CLIENT\token.txt") as f:
            token = f.read().strip()
    except FileNotFoundError:
        print("Could not find token.txt")
        return

    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            r = requests.get(f"{host}/list_tasks", headers=headers)
            if r.status_code == 200:
                tasks = r.json()
                print("\n- Task List ")
                if tasks:
                    for task in tasks:
                        print(f"  → {task}")
                        # Check and execute file_cleanup
                        if task.get("task_type") == "file_cleanup":
                            task_id = task.get("id")
                            if task_id:
                                file_cleanup(task_id)
                else:
                    print("  (no tasks)")
            else:
                print("Error:", r.status_code, r.text)
        except requests.exceptions.RequestException as e:
            print("Connection error:", e)
        
        time.sleep(interval)

poll_server()