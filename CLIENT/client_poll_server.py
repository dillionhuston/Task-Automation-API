import time
import requests

host = "http://localhost:8000"  

def poll_server(interval=10):
    try:
        with open("token.txt") as f: 
            token = f.read().strip()
    except FileNotFoundError:
        print("Could not find token.txt")
        return

    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            r = requests.get(f"{host}/list_tasks", headers=headers)
            if r.status_code == 200:
                print("\n- Task List ")
                print(r.json())
            else:
                print("Error:", r.status_code, r.text)
        except requests.exceptions.RequestException as e:
            print("Connection error:", e)
        
        time.sleep(interval)
