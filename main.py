import time
from crypto import crypto_extractor
from stock import stock_extractor
from common.db import write_db
from datetime import datetime, timezone


tickers = [
    "ABEV3", "B3SA3", "BBAS3", "BBDC4", "BHIA3", "BOVA11", "BOVV11", "BPAC11",
    "CSNA3", "EMBR3", "GGBR4", "HAPV3", "ITUB4", "LREN3", "MGLU3", "NTCO3",
    "PETR4", "PRIO3", "RENT3", "SMAL11", "SUZB3", "USIM5", "VALE3", "WEGE3"
]


if __name__ == "__main__":
    while True:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        # crypto
        for coin in ['BTC', 'ETH', 'SOL', 'PAXG']:
            data = crypto_extractor.extract_coin(coin)
            if data:
                blob_name = f"crypto/{coin}_{timestamp}.json"
                write_db("grt_raw", blob_name, data)
            else:
                print(f"⚠️ {coin} not saved")

        # stock
        for ticker in tickers:
            data = stock_extractor.get_stock_data_yf(ticker)
            if data:
                blob_name = f"stock/{ticker}_{timestamp}.json"
                write_db("grt_raw", blob_name, data)
                time.sleep(1)


        time.sleep(15 * 60)  # waits 15min before next running