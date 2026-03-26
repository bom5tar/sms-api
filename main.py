from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="SMS Viewer API")


class IncomingSMS(BaseModel):
    sender: Optional[str] = None
    message_text: str
    received_at: Optional[str] = None
    user_id: Optional[str] = None


messages_store = []


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.post("/api/sms/inbound")
def receive_sms(payload: IncomingSMS):
    message_data = {
        "sender": payload.sender,
        "message_text": payload.message_text,
        "received_at": payload.received_at,
        "user_id": payload.user_id,
    }

    messages_store.append(message_data)

    return {
        "status": "saved",
        "message": message_data
    }


@app.get("/messages")
def get_messages():
    return {
        "count": len(messages_store),
        "messages": messages_store
    }
