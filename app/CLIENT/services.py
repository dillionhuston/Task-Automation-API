import requests
import time

host = 'http://127.0.0.1:8000'


# poll server



def signup(email, password, username):
    data = {"email": email, "password": password, "username": username}
    r = requests.post(f"{host}/register", json=data)
    print(r.json())

def login(email, password):
    data = {"username": email, "password": password}  
    r = requests.post(f"{host}/login", data=data)
    resp = r.json()
    token = resp.get("access_token")

    if not token:
        print("Login failed:", resp)
        return None
    print(f"Token: {token}")

    with open("token.txt", "w") as f:
        f.write(token)
    return token



def create_task(task_type, schedule_time, receiver_email, title):
    print("Creating task")
    try:
        with open(r"C:\Users\amazo\Desktop\Projects\Network_monitor\Task-Automation-API\Task-Automation-API\app\CLIENT\token.txt") as f:
            token = f.read().strip()
            print("Found token")
    except FileNotFoundError:
        print("Token file not found. Please log in first.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "task_type": task_type,
        "schedule_time": schedule_time,
        "receiver_email": receiver_email,
        "title": title
    }

    url = f"{host}/schedule"

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)  # 10-second timeout
    except requests.exceptions.Timeout:
        print("Request timed out. The server may be down or unreachable.")
        return
    except requests.exceptions.RequestException as e:
        print("Error sending request:", e)
        return

    try:
        resp = r.json()
    except Exception:
        resp = r.text  # fallback

    if r.status_code == 200:
        print("Task scheduled successfully")
    else:
        print("Failed to schedule task:", r.status_code, resp)
