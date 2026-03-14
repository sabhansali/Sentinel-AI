from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

# Correct absolute import
from ai_risk_engine.detection.ast_engine.engine import sanitize_code

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

class CodeRequest(BaseModel):
    code: str

@app.post("/sanitize")
def sanitize_endpoint(request: CodeRequest):
    result = sanitize_code(request.code)
    if result["status"] == "success":
        return {
            "sanitized_code": result["sanitized_code"],
            "mapping": result["mapping"]
        }
    else:
        return {"error": result["message"]}