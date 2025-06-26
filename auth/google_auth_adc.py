import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth.transport.requests

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CLIENT_SECRETS_FILE = "/Users/andregortari/Desktop/currency_monitor/client_secret.json"  # ajuste o caminho do seu arquivo
TOKEN_PATH = Path.home() / ".config/gcloud/application_default_credentials.json"

def authenticate_with_google():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    # Refresh para garantir validade completa do token
    creds.refresh(google.auth.transport.requests.Request())

    # Cria pasta se não existir e salva ADC
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as token_file:
        token_file.write(creds.to_json())

    print(f"✅ Autenticado e credenciais ADC salvas em {TOKEN_PATH}")

if __name__ == "__main__":
    authenticate_with_google()
