import requests
from datetime import datetime

def extract_coin(coin='BTC', currency='USD'):
    try:
        url = f"https://api.coinbase.com/v2/prices/{coin}-{currency}/spot"
        response = requests.get(url)
        response.raise_for_status()  # raise error for status != 200
        data = response.json()
        return {
            "source": "Coinbase",
            "coin": data['data']['base'],
            "currency": data['data']['currency'],
            "value": float(data['data']['amount']),
            "timestamp": datetime.now().isoformat()
        }
    except requests.RequestException as e:
        print(f"❌ Error fetching {coin}: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"❌ Error processing {coin}: {e}")
        return None
