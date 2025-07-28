# em configurar_webhook.py

import requests
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis do seu arquivo .env
load_dotenv()

API_URL = os.getenv("EVOLUTION_API_URL")
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = os.getenv("EVOLUTION_INSTANCE_NAME")

# O endereço do seu bot (rodando no seu PC) que o Docker vai acessar
WEBHOOK_URL_PARA_CONFIGURAR = "https://87a6c479f64e.ngrok-free.app/webhook"


def definir_webhook_final():
    """
    Envia a requisição com o payload correto para definir o webhook.
    """
    endpoint = f"{API_URL}/webhook/set/{INSTANCE_NAME}"

    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }

    payload = {
        "enabled": True,
        "url": WEBHOOK_URL_PARA_CONFIGURAR
    }

    print(f"Configurando webhook com o payload final para a instância '{INSTANCE_NAME}'...")

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        print("\n--- SUCESSO! ---")
        print("Webhook configurado com sucesso. Resposta da API:")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"\n--- ERRO ---")
        print(f"Não foi possível configurar o webhook: {e}")
        if e.response:
            print(f"Resposta da API: {e.response.text}")

# --- Ponto de Execução ---
if __name__ == "__main__":
    definir_webhook_final()