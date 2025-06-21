from datetime import datetime
import yfinance as yf

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
            "value": round(last_quote["Close"], 2),
            "high": round(last_quote["High"], 2),
            "low": round(last_quote["Low"], 2),
            "volume": int(last_quote["Volume"]),
            "timestamp": last_quote.name.isoformat()
        }

    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return None
