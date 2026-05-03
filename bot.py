import os
import django
import time
import pandas as pd

# 🔥 setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from trading.models import Strategy, Trade
from trading.services.iq import IQService
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TIMEFRAME = 60


def get_candles(iq, asset):
    candles = iq.api.get_candles(asset, TIMEFRAME, 100, time.time())
    df = pd.DataFrame(candles)
    df["close"] = df["close"].astype(float)
    return df


def analyze(df):
    ema20 = EMAIndicator(df["close"], 20).ema_indicator()
    ema50 = EMAIndicator(df["close"], 50).ema_indicator()
    rsi = RSIIndicator(df["close"], 14).rsi()

    last_ema20 = ema20.iloc[-1]
    last_ema50 = ema50.iloc[-1]
    last_rsi = rsi.iloc[-1]

    if last_ema20 > last_ema50 and last_rsi < 60:
        return "call"

    if last_ema20 < last_ema50 and last_rsi > 40:
        return "put"

    return None


def run():
    print("🤖 BOT iniciado...")

    while True:
        strategies = Strategy.objects.filter(active=True)

        for s in strategies:
            try:
                print(f"📊 Analizando {s.asset}")

                iq = IQService(mode=s.mode)

                df = get_candles(iq, s.asset)

                signal = analyze(df)

                if not signal:
                    print("⏸️ Sin señal")
                    continue

                print(f"🚀 Ejecutando {signal}")

                trade = Trade.objects.create(
                    asset=s.asset,
                    direction=signal,
                    amount=s.amount,
                    status="pending",
                    mode=s.mode
                )

                result = iq.execute_trade(s.asset, signal, s.amount)

                trade.result = result["result"]
                trade.profit = result["profit"]
                trade.status = "executed"
                trade.save()

                print(f"✅ Resultado: {result}")

                time.sleep(s.timeframe)

            except Exception as e:
                print(f"❌ Error: {e}")

        time.sleep(10)


if __name__ == "__main__":
    run()