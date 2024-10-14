# Helper/telegram_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')


def send_message(chat_id: int, message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    headers = {"Content-Type": "application/json"}
    requests.request("POST", url, json=payload, headers=headers)


def send_photo(chat_id: int, photo_url: str, caption: str = '') -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)
