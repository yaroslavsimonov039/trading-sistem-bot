import os
import sqlite3
from datetime import datetime


DATA_FOLDER = "full_db"
DB_FILE = "prices.db"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DB_NAME = os.path.join(DATA_FOLDER, DB_FILE)

def save_price(price: float):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO prices (price, timestamp) VALUES (?, ?)",
        (price, timestamp)
    )

    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def get_last_n_prices(n=100):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT price FROM prices ORDER BY id DESC LIMIT ?", (n,))
    rows = cur.fetchall()

    conn.close()
    return [r[0] for r in rows][::-1]
