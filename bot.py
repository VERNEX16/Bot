import requests
import time
import sqlite3
import random
import string

BOT_TOKEN = "8661307520:AAH7Mw3WrR63PPmK_EIy0LW8oz4r50bW6Fs"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

BASE_API = "https://your-app-name.onrender.com/api/numinfo"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT, expires REAL)")
    conn.commit()
    conn.close()

def create_key(days):
    key = "VERNEX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    expiry = time.time() + (days * 86400) if days != 0 else 9999999999

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO keys VALUES (?, ?)", (key, expiry))
    conn.commit()
    conn.close()

    return key

def send(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def get_updates(offset=None):
    return requests.get(f"{API_URL}/getUpdates", params={"offset": offset}).json()

init_db()
last_id = None

while True:
    updates = get_updates(last_id)

    for u in updates.get("result", []):
        last_id = u["update_id"] + 1

        if "message" not in u:
            continue

        chat_id = u["message"]["chat"]["id"]
        text = u["message"].get("text", "")

        if text == "/start":
            send(chat_id, "Choose:\n/1day\n/2day\n/lifetime")

        elif text in ["/1day", "/2day", "/lifetime"]:
            days = 1 if text=="/1day" else 2 if text=="/2day" else 0
            key = create_key(days)

            url = f"{BASE_API}?num=7000000000&key={key}"

            send(chat_id, f"KEY: {key}\n\nURL:\n{url}")

    time.sleep(2)
