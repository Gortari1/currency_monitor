import os
import streamlit as st
from tinydb import TinyDB
from collections import defaultdict
import humanize
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# --- Carrega dados ---
db = TinyDB('db.json')
data = db.all()

# --- Helper functions ---
def file_size(path='db.json'):
    size_bytes = os.path.getsize(path)
    return humanize.naturalsize(size_bytes)

def get_last_price(data):
    latest = {}
    for item in data:
        key = item.get("coin") or item.get("asset")
        if key:
            ts = item.get("timestamp")
            if key not in latest or ts > latest[key]["timestamp"]:
                latest[key] = item
    return latest

def to_dataframe(data):
    records = []
    for item in data:
        key = item.get("coin") or item.get("asset")
        if not key:
            continue
        timestamp = item.get("timestamp")
        try:
            dt = datetime.fromisoformat(timestamp)
        except:
            continue
        records.append({
            "name": key,
            "value": float(item["value"]),
            "source": item["source"],
            "timestamp": dt
        })
    return pd.DataFrame(records)

# --- Preparar dataframe ---
df = to_dataframe(data)
cryptos_df = df[df["source"] == "Coinbase"]
stocks_df = df[df["source"] != "Coinbase"]

# --- Layout de quadrantes ---
st.title("📊 Asset Dashboard")

# === QUADRANTE 1 (SUPERIOR ESQUERDO) ===
st.subheader("📌 Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("📄 Total Registros", len(data))
    st.metric("💽 Tamanho do DB", file_size())
    st.metric("💱 Nº Moedas Diferentes", df['name'].nunique())

# === QUADRANTE 2 (SUPERIOR DIREITO) ===
st.subheader("📈 Cripto - Preço ao Longo do Tempo")
if not cryptos_df.empty:
    crypto_pivot = cryptos_df.pivot(index="timestamp", columns="name", values="value")
    st.line_chart(crypto_pivot)
else:
    st.info("Sem dados de criptomoedas.")

# === QUADRANTE 3 (INFERIOR ESQUERDO) ===
st.subheader("📃 Lista de Ações")
with st.expander("Clique para ver todas as ações registradas"):
    last_prices = get_last_price(stocks_df.to_dict(orient="records"))
    for name, item in sorted(last_prices.items()):
        st.write(f"**{name}** → `{item['value']} {item['currency']}` em `{item['timestamp']}`")

# === QUADRANTE 4 (INFERIOR DIREITO) ===
st.subheader("📉 Ações - Preço ao Longo do Tempo")
if not stocks_df.empty:
    stocks_pivot = stocks_df.pivot(index="timestamp", columns="name", values="value")
    st.line_chart(stocks_pivot)
else:
    st.info("Sem dados de ações.")
