import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_URL = os.getenv("EVOLUTION_API_URL")
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = os.getenv("EVOLUTION_INSTANCE_NAME")

def enviar_mensagem(numero, texto):
    """Envia uma mensagem de texto para um contato."""
    
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }
    
    payload = {
        "number": numero,
        "text": texto,
    }
    
    endpoint = f"{API_URL}/message/sendText/{INSTANCE_NAME}"
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status() # Lança um erro para status codes ruins (4xx ou 5xx)
        print(f"Mensagem enviada com sucesso para {numero}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para a Evolution API: {e}")
        return None