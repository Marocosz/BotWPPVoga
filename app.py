import requests
import json

# --- Suas Configurações ---
API_URL = "http://localhost:8080"
INSTANCE_NAME = "teste1"
API_KEY = "D3E21DB11962-4CED-8B4A-1950EBC5E46C"  # Sua chave API

# --- Dados da Mensagem ---
# ⬇️ Altere o número e a mensagem conforme precisar ⬇️
numero_para_enviar = "5534991717463"
mensagem_para_enviar = "Vtnc rhuan"

def enviar_mensagem_correta(numero, texto):
    """Envia a mensagem usando a estrutura de payload correta."""
    
    print(f"Enviando para '{numero}' com a estrutura correta...")
    
    endpoint = f"{API_URL}/message/sendText/{INSTANCE_NAME}"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }
    
    # Payload baseado na documentação que você encontrou.
    # A mudança crucial está aqui: 'text' está no nível principal.
    payload = {
        "number": numero,
        "text": texto,
        "delay": 1200 # Parâmetro opcional do exemplo
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        print("--- Resposta da API ---")
        print(f"Status Code: {response.status_code}")
        # Tenta formatar a resposta como JSON, senão mostra como texto
        try:
            print(json.dumps(response.json(), indent=2))
        except json.JSONDecodeError:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: {e}")

# --- Ponto de Execução ---
if __name__ == "__main__":
    enviar_mensagem_correta(numero_para_enviar, mensagem_para_enviar)