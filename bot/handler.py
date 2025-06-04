import requests
import time
from utils.logger import log_message

def send_message(user_id, message, delay=0, bot_token=None):
    if delay > 0:
        time.sleep(delay)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": user_id, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        log_message("Sent", user_id, message)
    else:
        print(f"[ERROR] Failed to send message to {user_id}: {response.status_code}, {response.text}")

def fetch_updates(offset=None, bot_token=None):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {"offset": offset, "timeout": 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"[ERROR] Failed to fetch updates: {response.status_code}, {response.text}")
        return []
