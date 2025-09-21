import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8080"
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = "marcos-dev-test" 

HEADERS = {"apikey": API_KEY, "Content-Type": "application/json"}

def clean_number(number_jid: str) -> str:
    """Garante que estamos usando apenas o número, sem o sufixo do JID."""
    return number_jid.split('@')[0]

def send_text(number: str, text: str):
    """Envia uma mensagem de texto simples."""
    endpoint = f"{API_URL}/message/sendText/{INSTANCE_NAME}"
    payload = {
        "number": clean_number(number),
        "options": { "presence": "composing" },
        "text": text
    }
    try:
        response = requests.post(endpoint, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        print(f"Mensagem de texto enviada para {clean_number(number)}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar texto para {clean_number(number)}: {e}")
        if e.response is not None:
            try: 
                print(f"Resposta de erro da Evolution API: {e.response.json()}")
            except json.JSONDecodeError: 
                print(f"Resposta de erro da Evolution API (não-JSON): {e.response.text}")
        return None