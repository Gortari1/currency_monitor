import yfinance as yf
from datetime import datetime, timedelta
from tinydb import TinyDB

db = TinyDB("historicalDb.json")

COINS = {
    "BTC-USD": "BTC",
    "ETH-USD": "ETH",
    "SOL-USD": "SOL",
    "PAXG-USD": "PAXG"
}

def ingest_yahoo_history():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 24 meses

    for ticker, symbol in COINS.items():
        print(f"⬇️ loading historical {symbol} via Yahoo Finance")
        data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"),
                           progress=True)
        for idx, row in data.iterrows():
            db.insert({
                "source": "Yahoo Finance",
                "coin": symbol,
                "currency": "USD",
                "value": float(round(row['Close'])),
                "timestamp": idx.isoformat()
            })
        print(f"✅ {symbol} saved")


if __name__ == "__main__":
    ingest_yahoo_history()
