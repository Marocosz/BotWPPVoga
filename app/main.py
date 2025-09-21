# Em app/main.py
from fastapi import FastAPI
from app import bot_logic
from app.models import WebhookPayload # <--- IMPORTANTE: Importa o modelo

app = FastAPI(title="Bot para Clínica de Estética Voga")

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload): # <--- IMPORTANTE: Usa o modelo para validação
    """Recebe webhooks da Evolution API e os processa."""
    
    # Graças ao Pydantic, já sabemos que o 'payload' tem a estrutura correta.
    # A lógica de filtragem agora pode ser feita diretamente no bot_logic.
    if payload.event == 'messages.upsert' and not payload.data.key.fromMe:
        bot_logic.process_message(payload) # Enviamos o payload completo
            
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Bot da Clínica de Estética Voga está no ar!"}