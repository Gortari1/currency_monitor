import threading
import time
from datetime import datetime, timezone

from auth.google_auth_adc import authenticate_with_google
from front.app import DashboardApp
from crypto import crypto_extractor
from stock import stock_extractor
from common.db import write_db

tickers = [
    "ABEV3", "B3SA3", "BBAS3", "BBDC4", "BHIA3", "BOVA11", "BOVV11", "BPAC11",
    "CSNA3", "EMBR3", "GGBR4", "HAPV3", "ITUB4", "LREN3", "MGLU3", "NTCO3",
    "PETR4", "PRIO3", "RENT3", "SMAL11", "SUZB3", "USIM5", "VALE3", "WEGE3"
]

import customtkinter as ctk

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.authenticated = False
        self.title("Login")
        self.geometry("400x300")

        self.login_button = ctk.CTkButton(self, text="Login com Google", command=self.login)
        self.login_button.pack(pady=100)

    def login(self):
        try:
            authenticate_with_google()
            self.authenticated = True
            self.destroy()  # Fecha janela
        except Exception as e:
            print("Erro no login:", e)
            self.authenticated = False


def run_data_pipeline():
    while True:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        for coin in ['BTC', 'ETH', 'SOL', 'PAXG']:
            data = crypto_extractor.extract_coin(coin)
            if data:
                blob_name = f"crypto/{coin}_{timestamp}.json"
                write_db("grt_raw", blob_name, data)
            else:
                print(f"⚠️ {coin} not saved")

        for ticker in tickers:
            data = stock_extractor.get_stock_data_yf(ticker)
            if data:
                blob_name = f"stock/{ticker}_{timestamp}.json"
                write_db("grt_raw", blob_name, data)
                time.sleep(1)

        time.sleep(15 * 60)


def main():
    login_window = LoginWindow()
    login_window.mainloop()

    if login_window.authenticated:
        threading.Thread(target=run_data_pipeline, daemon=True).start()

        app = DashboardApp()
        app.mainloop()
    else:
        print("❌ Login falhou ou foi cancelado.")


if __name__ == "__main__":
    main()
