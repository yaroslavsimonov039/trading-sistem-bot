import sqlite3

TRADE_DB = "trades.db"
FULL_DB = "full_db/prices.db"

def get_trade_conn():
    return sqlite3.connect(TRADE_DB, check_same_thread=False)

def get_full_conn():
    return sqlite3.connect(FULL_DB, check_same_thread=False)

def init_db():
    conn = get_trade_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS position_types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """)
    cur.execute("INSERT OR IGNORE INTO position_types VALUES (1,'buy')")
    cur.execute("INSERT OR IGNORE INTO position_types VALUES (2,'sell')")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position_type_id INTEGER,
        price_id INTEGER,
        is_closed INTEGER DEFAULT 0,
        result TEXT,
        percent REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trade_indicators_snapshot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER,
        indicator_name TEXT,
        indicator_value REAL
    )
    """)
    conn.commit()
    conn.close()

def create_trade(position_type_id, price_id):
    conn = get_trade_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO trades (position_type_id, price_id, is_closed)
    VALUES (?, ?, 0)
    """, (position_type_id, price_id))
    trade_id = cur.lastrowid
    conn.commit()
    conn.close()
    return trade_id

def close_trade(trade_id, result, percent):
    conn = get_trade_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE trades
    SET is_closed=1, result=?, percent=?
    WHERE id=?
    """, (result, percent, trade_id))
    conn.commit()
    conn.close()
