from datetime import datetime, timedelta
from app import evolution
from app.models import WebhookPayload

# "Memória" temporária do bot. No futuro, isso será um banco de dados.
user_state = {}

def process_message(payload: WebhookPayload):
    """Processa um webhook de nova mensagem e decide qual ação tomar."""
    
    sender_jid = payload.data.key.remoteJid
    sender_name = payload.data.pushName

    if not sender_jid or "@s.whatsapp.net" not in sender_jid:
        return

    print(f"Processando evento de {sender_name} ({sender_jid})")

    last_time = user_state.get(sender_jid, {}).get('last_message_time')
    intervalo = timedelta(hours=1)
    current_time = datetime.now()

    if not last_time or (current_time - last_time) > intervalo:
        # É a primeira interação ou o contato retornou após o intervalo.
        print(f"Primeira mensagem de {sender_name} no intervalo. Enviando menu de boas-vindas.")
        
        # Envia o menu principal como texto
        welcome_message = (
            f"Olá, {sender_name}! Bem-vindo(a) à Clínica de Estética Voga.\n\n"
            "Como podemos te ajudar hoje?\n\n"
            "Digite o número da opção desejada:\n"
            "1️⃣  *Conhecer nossos serviços*\n"
            "2️⃣  *Agendar um horário*\n"
            "3️⃣  *Falar com um atendente*"
        )
        evolution.send_text(sender_jid, welcome_message)
        
        # Atualiza o estado do usuário
        user_state[sender_jid] = {
            'last_message_time': current_time,
            'stage': 'main_menu' # Guardamos o "estágio" da conversa
        }

    else:
        # Lógica para mensagens subsequentes, baseada no que o usuário DIGITOU
        
        # Extrai o texto limpo da resposta do usuário
        message_text = ""
        if payload.data.message and payload.data.message.conversation:
            message_text = payload.data.message.conversation.strip().lower() # .lower() para ignorar maiúsculas
        
        current_stage = user_state.get(sender_jid, {}).get('stage')

        if current_stage == 'main_menu':
            if message_text == '1' or "serviços" in message_text:
                servicos_texto = (
                    "Estes são os nossos principais serviços:\n\n"
                    "💆‍♀️ *Limpeza de Pele Profunda* - R$ 150,00\n"
                    "✨ *Massagem Modeladora* - R$ 120,00\n"
                    "✒️ *Design de Sobrancelhas* - R$ 70,00\n\n"
                    "Para agendar um destes serviços, digite *2*."
                )
                evolution.send_text(sender_jid, servicos_texto)
            
            elif message_text == '2' or "agendar" in message_text:
                evolution.send_text(sender_jid, "Ótimo! Para qual dos nossos serviços você gostaria de agendar um horário?")
                user_state[sender_jid]['stage'] = 'agendando_servico'
            
            elif message_text == '3' or "atendente" in message_text:
                evolution.send_text(sender_jid, "Entendido. Um de nossos atendentes irá te responder nesta mesma conversa o mais breve possível.")
                user_state[sender_jid]['stage'] = 'aguardando_atendente'
            
            else:
                evolution.send_text(sender_jid, "Opção inválida. Por favor, digite *1*, *2* ou *3* para continuar.")
        
        # Atualiza a hora da última mensagem
        user_state.setdefault(sender_jid, {})['last_message_time'] = current_time