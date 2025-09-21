from pydantic import BaseModel
from typing import Optional, Dict

class WebhookMessageContent(BaseModel):
    """Modela o conteúdo de uma mensagem de texto."""
    conversation: Optional[str] = None
    extendedTextMessage: Optional[Dict] = None

class WebhookKey(BaseModel):
    """Modela a chave identificadora da mensagem."""
    remoteJid: str
    fromMe: bool
    id: str
    participant: Optional[str] = None

class WebhookData(BaseModel):
    """Modela o objeto 'data' principal do webhook."""
    key: WebhookKey
    pushName: Optional[str] = "Cliente"
    message: Optional[WebhookMessageContent] = None
    
class WebhookPayload(BaseModel):
    """Modela a estrutura completa do webhook que recebemos."""
    event: str
    instance: str
    data: WebhookData