from pydantic import BaseModel, Field
from typing import Optional, Any

class MessageKey(BaseModel):
    remoteJid: Optional[str] = None
    fromMe: Optional[bool] = False
    id: Optional[str] = None

class MessageData(BaseModel):
    key: MessageKey
    pushName: Optional[str] = None
    message: Optional[dict[str, Any]] = None
    messageType: Optional[str] = None
    messageTimestamp: Optional[int] = None

class WebhookPayload(BaseModel):
    instance: str
    event: str
    data: MessageData