from datetime import datetime
from enum import nonmember

import yfinance as yf

def parse_float(val):
    try:
        return float(val)
    except:
        return None


def get_stock_data_yf(ticker):
    try:
        stock = yf.Ticker(ticker + ".SA")
        data = stock.history(period="1d")

        if data.empty:
            print(f"⚠️ Nothing found for {ticker}")
            return None

        last_quote = data.iloc[-1]

        return {
            "source": "Yahoo Finance",
            "asset": ticker,
            "currency": "BRL",
            "value": parse_float(round(last_quote["Close"])),
            "high": parse_float(round(last_quote["High"])),
            "low": parse_float(round(last_quote["Low"])),
            "volume": parse_float(round(last_quote["Volume"])),
            "timestamp": last_quote.name.isoformat()
        }

    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return None
