import re
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="SMS Purchase API")


class IncomingSMS(BaseModel):
    sender: Optional[str] = None
    message_text: str
    received_at: Optional[str] = None
    user_id: Optional[str] = None


PURCHASE_KEYWORDS = [
    "purchase",
    "card purchase",
    "point of sale",
    "pos",
    "mada",
    "apple pay",
    "merchant",
    "spent",
    "debit card",
    "credit card",
    "payment",
    "purchase transaction",
    "point-of-sale",
    "purchase using card",
    "شراء",
    "عملية شراء",
    "مشتريات",
    "نقطة بيع",
    "مدى",
]

NON_PURCHASE_KEYWORDS = [
    "otp",
    "verification code",
    "password",
    "login",
    "sign in",
    "transfer",
    "deposit",
    "refund",
    "reversal",
    "withdrawal",
    "balance",
    "promotion",
    "offer",
    "discount",
    "رمز تحقق",
    "تحويل",
    "إيداع",
    "استرداد",
    "سحب",
    "رصيدك",
]


def classify_message(text: str) -> str:
    t = text.lower()

    for word in NON_PURCHASE_KEYWORDS:
        if word.lower() in t:
            return "non_purchase"

    for word in PURCHASE_KEYWORDS:
        if word.lower() in t:
            return "purchase"

    return "unknown"


def extract_amount_currency(text: str):
    match = re.search(r'(\d+(?:\.\d{1,2})?)\s*(SAR|SR|ر\.س|ريال)', text, re.IGNORECASE)
    if match:
        amount = float(match.group(1))
        currency = match.group(2).upper()

        if currency in ["SR", "ر.س", "ريال"]:
            currency = "SAR"

        return f"{amount:.2f} {currency}"

    return None


def extract_time(text: str):
    match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)', text)
    if match:
        return match.group(1)
    return None


def extract_source(text: str):
    match = re.search(r'(?:from|من|لدى)\s+(.+?)(?:\s|$)', text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.post("/api/sms/inbound")
def receive_sms(payload: IncomingSMS):
    text = payload.message_text

    classification = classify_message(text)
    amount = extract_amount_currency(text)
    time = extract_time(text)
    source = extract_source(text)

    return {
        "status": "ok",
        "user_id": payload.user_id,
        "classification": classification,
        "amount": amount,
        "time": time,
        "source": source,
        "message_text": text
    }