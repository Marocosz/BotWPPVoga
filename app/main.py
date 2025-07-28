# em app/main.py

from fastapi import FastAPI, Request
from .models import WebhookPayload  # Nossos modelos de dados Pydantic
from . import api_client           # Nosso cliente para falar com a Evolution API
import json
import time

app = FastAPI(
    title="Bot de Atendimento Voga",
    description="Um bot para automatizar o atendimento via WhatsApp usando a Evolution API.",
    version="1.0.0"
)

# --- "MEMÓRIA" DO NOSSO BOT ---
# Um dicionário para guardar o estado da conversa de cada usuário.
# Exemplo: { "55349...": "aguardando_opcao_menu", "55119...": "agendando" }
conversas_ativas = {}
# -----------------------------

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"status": "online", "message": "Bem-vindo ao Bot da Clínica Voga!"}


@app.post("/webhook", tags=["Webhook"])
async def webhook_receiver(request: Request):
    """
    Recebe todas as notificações, filtra e processa apenas as que nos interessam.
    """
    payload_bruto = await request.json()

    # Filtro principal: só nos importamos com eventos de novas mensagens.
    if payload_bruto.get("event") != "messages.upsert":
        return {"status": "evento nao processado"}
    
    # Tentamos validar a estrutura dos dados. Se falhar, ignoramos.
    try:
        payload = WebhookPayload.parse_obj(payload_bruto)
    except Exception as e:
        print(f"!!! Erro de validação Pydantic: {e} !!!")
        return {"status": "evento com erro de validação"}

    # A partir daqui, temos um payload de mensagem válido e podemos processá-lo.
    try:
        remetente = payload.data.key.remoteJid

        # --- FILTROS DE SEGURANÇA E CONTEXTO ---

        # 1. Ignora mensagens de grupo
        if "@g.us" in remetente:
            print("mensagem ignorada (grupo)")
            return {"status": "mensagem ignorada (grupo)"}

        # 2. Ignora mensagens enviadas pelo próprio bot (essencial para produção)
        if payload.data.key.fromMe:
            print("mensagem ignorada (propria)")
            return {"status": "mensagem ignorada (propria)"}
        
        # 3. Ignora mensagens antigas para manter a conversa em tempo real
        current_timestamp = int(time.time())
        message_timestamp = payload.data.messageTimestamp
        if message_timestamp and (current_timestamp - (message_timestamp or 0) > 120):
            print(f"AVISO: Mensagem de {remetente} ignorada por ser muito antiga.")
            return {"status": "mensagem antiga ignorada"}

        # --- PROCESSAMENTO DA MENSAGEM ---
        message_content = payload.data.message or {}
        mensagem_recebida = message_content.get("conversation", "").lower().strip()
        nome_contato = payload.data.pushName or "Cliente"
        
        print(f"Processando mensagem de '{nome_contato}' ({remetente}): '{mensagem_recebida}'")

        estado_atual = conversas_ativas.get(remetente, "inicio")

        # --- LÓGICA DO BOT BASEADA EM ESTADOS (O CÉREBRO) ---

        # ESTADO 1: Início da conversa
        if estado_atual == "inicio" and (mensagem_recebida in ["oi", "olá", "ola", "bom dia"]):
            texto_resposta = (
                f"Olá, {nome_contato}! Bem-vindo(a) à Clínica Voga. 😊\n\n"
                "Digite o número da opção desejada:\n\n"
                "*1.* Conhecer nossos serviços\n"
                "*2.* Agendar uma avaliação\n"
                "*3.* Falar com um atendente"
            )
            api_client.enviar_mensagem(remetente, texto_resposta)
            # Atualiza o estado: agora estamos esperando uma resposta para o menu
            conversas_ativas[remetente] = "aguardando_opcao_menu"

        # ESTADO 2: Aguardando a escolha do menu
        elif estado_atual == "aguardando_opcao_menu":
            if mensagem_recebida == "1":
                texto_resposta = (
                    "Nossos principais serviços são:\n\n"
                    "- Limpeza de Pele Profunda\n"
                    "- Botox e Preenchimento\n"
                    "- Depilação a Laser\n\n"
                    "Para retornar ao menu principal, envie *oi*."
                )
                api_client.enviar_mensagem(remetente, texto_resposta)
                conversas_ativas[remetente] = "inicio"
            
            elif mensagem_recebida == "2":
                texto_resposta = "Ótima escolha! Para agendar sua avaliação, por favor, me diga o melhor dia e período (manhã/tarde) para você."
                api_client.enviar_mensagem(remetente, texto_resposta)
                conversas_ativas[remetente] = "agendando_dia"
            
            elif mensagem_recebida == "3":
                texto_resposta = "Ok! Estou transferindo sua conversa para um de nossos atendentes. Por favor, aguarde um momento."
                api_client.enviar_mensagem(remetente, texto_resposta)
                conversas_ativas.pop(remetente, None) # Remove o estado, finaliza o bot
            
            else:
                texto_resposta = "Opção inválida. Por favor, digite apenas o número (1, 2 ou 3)."
                api_client.enviar_mensagem(remetente, texto_resposta)
        
        # ESTADO 3 (Exemplo futuro): Agendando o dia
        elif estado_atual == "agendando_dia":
            # Aqui você processaria a resposta do dia/período e continuaria a conversa
            texto_resposta = f"Ok, anotado! Buscando horários para '{mensagem_recebida}'. Só um momento..."
            api_client.enviar_mensagem(remetente, texto_resposta)
            conversas_ativas[remetente] = "inicio" # Exemplo, voltaria para o início

        # RESPOSTA PADRÃO: Se não se encaixar em nenhuma regra
        else:
            texto_resposta = (
                "Desculpe, não entendi sua mensagem. 🤔\n"
                "Para ver as opções de atendimento, por favor, envie *oi*."
            )
            api_client.enviar_mensagem(remetente, texto_resposta)
            conversas_ativas[remetente] = "inicio"

    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")

    return {"status": "processado"}