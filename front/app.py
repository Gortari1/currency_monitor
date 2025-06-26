import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from google.cloud import storage
import json
import os
from datetime import datetime
import pytz

# Ativos
CRYPTO_ASSETS = ["BTC", "ETH", "PAXG"]
STOCK_ASSETS = [
    "ABEV3", "B3SA3", "BBAS3", "BBDC4", "BHIA3", "BOVA11", "BOVV11", "BPAC11",
    "CSNA3", "EMBR3", "GGBR4", "HAPV3", "ITUB4", "LREN3", "MGLU3", "NTCO3", "PETR4",
    "PRIO3", "RENT3", "SMAL11", "SUZB3", "USIM5", "VALE3", "WEGE3"
]

# Inicialização do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crypto & Stocks Dashboard")
        self.geometry("1200x800")

        self.crypto_data = {}
        self.stock_data = {}

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(padx=10, pady=10, fill="x")

        self.load_data()
        self.draw_chart()
        self.display_info()

    def load_data(self):
        client = storage.Client()
        bucket = client.bucket("grt_raw")

        # Carrega a última entrada de cada ativo
        blobs = list(bucket.list_blobs(prefix="crypto/")) + list(bucket.list_blobs(prefix="stock/"))
        latest_files = {}
        for blob in blobs:
            asset = blob.name.split("/")[-1].split("_")[0]
            if asset not in latest_files or blob.updated > latest_files[asset].updated:
                latest_files[asset] = blob

        for asset, blob in latest_files.items():
            content = blob.download_as_text()
            data = json.loads(content)
            if asset in CRYPTO_ASSETS:
                self.crypto_data[asset] = data
            elif asset in STOCK_ASSETS:
                self.stock_data[asset] = data

    def draw_chart(self):
        fig, ax = plt.subplots(figsize=(10, 5))
        now = datetime.now(pytz.utc)

        for coin, data in self.crypto_data.items():
            ax.plot([now], [data["value"]], label=coin)

        for stock, data in self.stock_data.items():
            ax.plot([now], [data["value"]], label=stock)

        ax.set_title("Últimos valores - Criptomoedas e Ações")
        ax.legend()
        ax.grid(True)

        chart = FigureCanvasTkAgg(fig, master=self.plot_frame)
        chart.get_tk_widget().pack(fill='both', expand=True)
        chart.draw()

    def display_info(self):
        def format_line(data_dict):
            lines = []
            for asset, data in sorted(data_dict.items()):
                delta = data["value"] - data.get("low", data["value"])  # fallback para cripto
                arrow = "▲" if delta > 0 else "▼"
                color = "green" if delta > 0 else "red"
                lines.append(f"{asset}: {data['value']:.2f}  {arrow}")
            return lines

        crypto_label = ctk.CTkLabel(self.info_frame, text="\n".join(format_line(self.crypto_data)), justify="left")
        crypto_label.pack(side="left", padx=20, pady=10)

        stock_label = ctk.CTkLabel(self.info_frame, text="\n".join(format_line(self.stock_data)), justify="left")
        stock_label.pack(side="right", padx=20, pady=10)


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
