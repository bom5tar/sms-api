@app.post("/api/sms")
def receive_sms(payload: IncomingSMS):
    message_data = {
        "sender": payload.sender,
        "message_text": payload.message_text,
        "received_at": payload.received_at,
        "user_id": payload.user_id,
    }

    messages_store.append(message_data)

    print("NEW MESSAGE RECEIVED")
    print("sender:", repr(payload.sender))
    print("message_text:", repr(payload.message_text))
    print("received_at:", repr(payload.received_at))
    print("user_id:", repr(payload.user_id))
    print("-" * 40)

    return {
        "status": "saved",
        "message": message_data
    }
