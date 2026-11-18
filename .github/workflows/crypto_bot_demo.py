import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import ccxt


def ema(values, period):
    if len(values) < period:
        raise ValueError(f"Dati insufficienti per EMA{period}")
    alpha = 2 / (period + 1)
    result = float(values[0])
    for value in values[1:]:
        result = alpha * float(value) + (1 - alpha) * result
    return result


def rsi(values, period=14):
    if len(values) <= period:
        raise ValueError("Dati insufficienti per RSI")
    changes = [float(values[i]) - float(values[i - 1]) for i in range(1, len(values))]
    recent = changes[-period:]
    avg_gain = sum(max(change, 0) for change in recent) / period
    avg_loss = sum(max(-change, 0) for change in recent) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def notify_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram non configurato: salto la notifica.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    request = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            print(f"Telegram: HTTP {response.status}")
    except Exception as exc:
        print(f"Errore nell'invio Telegram: {exc}")


def main():
    symbol = os.getenv("SYMBOL", "BTC/EUR")
    exchange_id = os.getenv("EXCHANGE_ID", "binance")
    exchange_class = getattr(ccxt, exchange_id, None)
    if exchange_class is None:
        raise ValueError(f"Exchange non supportato da CCXT: {exchange_id}")

    exchange = exchange_class({"enableRateLimit": True, "timeout": 20000})
    candles = exchange.fetch_ohlcv(symbol, timeframe="15m", limit=100)
    if len(candles) < 60:
        raise RuntimeError("L'exchange ha restituito poche candele.")

    # Esclude la candela più recente, che potrebbe essere ancora in formazione.
    closed_candles = candles[:-1]
    closes = [float(candle[4]) for candle in closed_candles]
    price = closes[-1]

    ema20 = ema(closes[-50:], 20)
    ema50 = ema(closes[-50:], 50)
    rsi14 = rsi(closes, 14)

    if ema20 > ema50 and 50 <= rsi14 <= 65 and price > ema20:
        signal = "POSSIBILE SEGNALE LONG (solo simulazione)"
    else:
        signal = "ATTENDERE"

    candle_time = datetime.fromtimestamp(
        closed_candles[-1][0] / 1000, tz=timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")

    message = (
        "BOT CRYPTO - SOLO DEMO\n"
        f"Mercato: {symbol}\n"
        f"Candela chiusa: {candle_time}\n"
        f"Prezzo di chiusura: {price:.2f} EUR\n"
        f"EMA20: {ema20:.2f}\n"
        f"EMA50: {ema50:.2f}\n"
        f"RSI14: {rsi14:.2f}\n"
        f"Segnale: {signal}\n"
        "Nessun ordine reale eseguito."
    )
    print(message)
    notify_telegram(message)


if __name__ == "__main__":
    main()
