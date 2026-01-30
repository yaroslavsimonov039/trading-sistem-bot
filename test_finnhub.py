import sqlite3

DB_PATH = "trades.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("Cleaning trades database...")

# 1️⃣ Видалити всі трейди
cur.execute("DELETE FROM trades")
print("✓ trades cleared")


# 3️⃣ Видалити таблицю снепшотів повністю
cur.execute("DROP TABLE IF EXISTS trade_indicators_snapshot")
print("✓ trade_indicators_snapshot table dropped")

# 4️⃣ Скинути AUTOINCREMENT (щоб id знову з 1 починались)
cur.execute("DELETE FROM sqlite_sequence WHERE name='trades'")
cur.execute("DELETE FROM sqlite_sequence WHERE name='trade_indicators_snapshot'")

conn.commit()
conn.close()

print("DONE ✅")



