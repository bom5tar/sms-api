from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Server is running"}


@app.post("/api/sms")
async def receive_sms(request: Request):
    body = await request.body()
    text = body.decode("utf-8").strip()

    print("NEW MESSAGE:", text)

    return {
        "status": "ok",
        "message_received": text
    }
