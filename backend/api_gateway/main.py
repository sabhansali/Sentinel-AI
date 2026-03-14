from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

events = []

@app.post("/ai-usage")
def receive_event(data: dict):

    event = {
        "device": data["device_id"],
        "tool": data["tool"],
        "domain": data["domain"],
        "time": datetime.now().strftime("%H:%M:%S")
    }

    events.append(event)

    print("\n🚨 ADMIN ALERT")
    print(event)

    return {"status": "logged"}

@app.get("/events")
def get_events():
    return events