from tinydb import TinyDB

db = TinyDB('db.json')

def save(data):
    db.insert(data)
    print(f"✅ Dados salvos: {data}")
