import requests
import time
import threading
from full_trades.input_orders import trade_input_loop, update_latest_price_id
from full_trades.trades_db import init_db
from full_db.db import save_price
from full_db.count_indicator import save_indicators

INTERVAL = 60
API_URL = "https://cdn.moneyconvert.net/api/latest.json"
last_price = None


init_db()

def process_new_price(price):
    price_id = save_price(price)
    save_indicators(price_id)
    update_latest_price_id(price_id)

def get_eur_usd_price():
    try:
        r = requests.get(API_URL, timeout=10)
        data = r.json()
        usd_to_eur = data["rates"]["EUR"]
        return round(1 / float(usd_to_eur), 6)
    except:
        return None

def price_loop():
    global last_price
    while True:
        price = get_eur_usd_price()
        if price and (last_price is None or price != last_price):
            process_new_price(price)
            last_price = price
        time.sleep(INTERVAL)

if __name__ == "__main__":
    threading.Thread(target=trade_input_loop, daemon=True).start()
    price_loop()
