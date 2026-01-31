from full_trades.trades_db import init_db, create_trade, close_trade
from full_trades.trades_db import (
    init_db,
    create_trade,
    close_trade
    )


latest_price_id = None

def update_latest_price_id(pid):
    global latest_price_id
    latest_price_id = pid

def trade_input_loop():
    init_db()  
    current_trade_id = None
    print("=== TRADE INPUT MODULE ===")

    while True:
        if current_trade_id is None:
            cmd = input("Open position? (buy / sell): ").lower().strip()
            if cmd not in ["buy", "sell"]:
                print("Only buy or sell")
                continue
            if latest_price_id is None:
                print(" No price yet")
                continue

            position_type_id = 1 if cmd == "buy" else 2
            current_trade_id = create_trade(position_type_id, latest_price_id)
            print(f" Position open: {cmd.upper()} | ID = {current_trade_id}")

        else:
            close_cmd = input("Did you close position? (yes): ").lower().strip()
            if close_cmd != "yes":
                continue

            result = input("Result? (profit / stop): ").lower().strip()
            if result not in ["profit", "stop"]:
                continue

            while True:
                try:
                    percent = float(input("How % result? "))
                    break
                except ValueError:
                    print("Put number.")

            close_trade(current_trade_id, result, percent)
            print("💾 Position saved.")
            current_trade_id = None
