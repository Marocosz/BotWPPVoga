from fastapi import FastAPI, Request
from .models import WebhookPayload  # Importa o modelo que criamos
import json

app = FastAPI(
    title="Bot de Atendimento para Clínica de Estética",
    description="Um bot para automatizar o atendimento via WhatsApp usando a Evolution API.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"status": "online", "message": "Bem-vindo ao Bot da Clínica Voga!"}

# --- NOSSO NOVO ENDPOINT DE WEBHOOK ---
@app.post("/webhook", tags=["Webhook"])
async def webhook_receiver(payload: WebhookPayload):
    """
    Recebe e processa as notificações (webhooks) da Evolution API.
    """
    print(">>> Webhook Recebido! <<<")
    
    # O Pydantic já validou os dados para nós. Agora podemos usá-los com segurança.
    # Usamos .dict() para converter o objeto Pydantic em um dicionário para impressão.
    print(json.dumps(payload.dict(), indent=2))
    
    # Por enquanto, apenas confirmamos o recebimento com status 200 (OK)
    return {"status": "recebido com sucesso"}