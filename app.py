# app.py

import requests
import json
from flask import Flask, request, jsonify
import os

# --- CONFIGURAÇÕES ---
# O bot vai pegar as configurações do ambiente do Docker Compose
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://evolution-api:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = "minha-instancia"
# --------------------

app = Flask(__name__)

def send_whatsapp_message(to_number, message_text):
    """Função para enviar uma mensagem de texto."""
    url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"
    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    payload = {
        "number": to_number,
        "textMessage": { "text": message_text }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        print(f"Resposta da API ao enviar para {to_number}: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para {to_number}: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Endpoint que recebe os webhooks da Evolution API."""
    webhook_data = request.json
    print("\n--- Webhook Recebido ---")
    print(json.dumps(webhook_data, indent=2))

    if (webhook_data.get('event') == 'messages.upsert' and 
        not webhook_data.get('data', {}).get('key', {}).get('fromMe')):
        
        try:
            sender = webhook_data['data']['key']['remoteJid']
            message_text = webhook_data['data']['message'].get('conversation') or \
                           webhook_data['data']['message'].get('extendedTextMessage', {}).get('text')

            if message_text:
                print(f"Mensagem recebida de {sender}: '{message_text}'")
                reply_text = f"Você disse: '{message_text}'"
                send_whatsapp_message(sender, reply_text)

        except KeyError as e:
            print(f"Erro ao processar o webhook: chave não encontrada - {e}")

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)