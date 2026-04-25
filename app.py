from flask import Flask, request, jsonify
import requests
import sqlite3
import time

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT, expires REAL)")
    conn.commit()
    conn.close()

def is_key_valid(key):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT expires FROM keys WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    if time.time() > row[0]:
        return False

    return True

init_db()

@app.route("/")
def home():
    return "Vernex API LIVE 🚀"

@app.route("/api/numinfo")
def numinfo():
    num = request.args.get("num")
    key = request.args.get("key")

    if not is_key_valid(key):
        return jsonify({"error": "Invalid or expired key"})

    try:
        res = requests.get(
            "https://cyber-osint-num-infos.vercel.app/api/numinfo",
            params={"num": num, "key": "Anonymous"}
        )

        data = res.json()

        # remove unwanted fields
        for k in list(data.keys()):
            if "owner" in k.lower() or "dm" in k.lower():
                data.pop(k)

        data["powered_by"] = "Vernex API ⚡"
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})
