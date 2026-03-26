from fastapi import FastAPI, Request

app = FastAPI(title="SMS Viewer API")

messages_store = []


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.post("/api/sms")
async def receive_sms(request: Request):
    data = await request.json()

    print("NEW MESSAGE RECEIVED")
    print("RAW DATA:", repr(data))
    print("-" * 40)

    messages_store.append(data)

    return {
        "status": "saved",
        "data": data
    }


@app.get("/messages")
def get_messages():
    return {
        "count": len(messages_store),
        "messages": messages_store
    }
    return {
        "count": len(messages_store),
        "messages": messages_store
    }
