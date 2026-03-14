import requests
from config import BACKEND_ENDPOINT, DEVICE_ID

def notify_backend(event):

    payload = {
        "device_id": DEVICE_ID,
        "tool": event["tool"],
        "domain": event["domain"]
    }

    try:

        requests.post(BACKEND_ENDPOINT, json=payload)

        print("📡 Sent to gateway")

    except Exception as e:

        print("Backend error:", e)