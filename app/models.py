from pydantic import BaseModel, Field
from typing import Optional, Any

# Usamos 'Optional' para campos que podem não existir em todos os eventos

class MessageKey(BaseModel):
    remoteJid: Optional[str] = None
    fromMe: Optional[bool] = False
    id: Optional[str] = None

class MessageData(BaseModel):
    key: MessageKey
    pushName: Optional[str] = None
    message: Optional[dict[str, Any]] = None # O conteúdo da mensagem pode variar muito
    messageType: Optional[str] = None

class WebhookPayload(BaseModel):
    instance: str
    event: str
    data: MessageData