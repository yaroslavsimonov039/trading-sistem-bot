import math
import sqlite3
from .db import get_last_n_prices, DB_NAME


def sma(period=14):
    prices = get_last_n_prices(period)
    prices = [float(p) for p in prices if p is not None and p != '']
    if len(prices) < period:
        return None
    return sum(prices) / period

def ema(period=14):
    prices = get_last_n_prices(period * 3)
    prices = [float(p) for p in prices if p is not None and p != '']
    if len(prices) < period:
        return None
    k = 2 / (period + 1)
    ema_val = prices[0]
    for price in prices[1:]:
        ema_val = price * k + ema_val * (1 - k)
    return ema_val

def rsi(period=14):
    prices = get_last_n_prices(period + 1)
    prices = [float(p) for p in prices if p is not None and p != '']
    if len(prices) < period + 1:
        return None

    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains)/period
    avg_loss = sum(losses)/period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def bollinger(period=20):
    prices = get_last_n_prices(period)
    prices = [float(p) for p in prices if p is not None and p != '']
    if len(prices) < period:
        return None

    mean = sum(prices)/period
    variance = sum((p-mean)**2 for p in prices)/period
    std = math.sqrt(variance)

    return mean, mean + 2*std, mean - 2*std



def save_indicators(price_id):
    sma_val = sma()
    ema_val = ema()
    rsi_val = rsi()
    boll = bollinger()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO indicators 
        (price_id, sma, ema, rsi, bollinger_mean, bollinger_upper, bollinger_lower)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        price_id,
        sma_val,
        ema_val,
        rsi_val,
        boll[0] if boll else None,
        boll[1] if boll else None,
        boll[2] if boll else None
    ))

    conn.commit()
    conn.close()
