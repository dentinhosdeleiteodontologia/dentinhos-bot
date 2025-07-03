# src/services/bot_logic.py

from src.models.conversation import db, Appointment

# Usamos um dicionário simples para guardar o estado da conversa de cada utilizador
# Numa aplicação real, isto poderia ser guardado no banco de dados para persistência
user_states = {}

class BotLogic:
    def process_message(self, message_text, phone_number):
        """
        Processa a mensagem recebida e retorna a resposta apropriada.
        """
        # Obtém o estado atual do utilizador ou define como 'initial' se for a primeira vez
        state = user_states.get(phone_number, 'initial')
        message_lower = message_text.lower().strip()
        response = ""

        # --- FLUXO DE CONVERSA PRINCIPAL ---

        if state == 'initial':
            response = (
                "Olá! Bem-vindo(a) à Dentinhos de Leite Odontologia. Como posso ajudar?\n\n"
                "1️⃣ - Agendar uma consulta\n"
                "2️⃣ - Ver informações do consultório\n"
                "3️⃣ - Falar com um humano"
            )
            user_states[phone_number] = 'awaiting_choice'

        elif state == 'awaiting_choice':
            if '1' in message_lower or 'agendar' in message_lower:
                response = "Ótimo! Para começar o agendamento, por favor, diga-me o nome completo do paciente."
                user_states[phone_number] = 'awaiting_patient_name'
            elif '2' in message_lower or 'informa' in message_lower:
                response = (
                    "Aqui estão as nossas informações:\n\n"
                    "📍 *Endereço:* Rua dos Sorrisos, 123, Bairro Feliz\n"
                    "⏰ *Horário:* Segunda a Sexta, das 9h às 18h\n"
                    "📞 *Telefone:* (11) 98765-4321\n\n"
                    "Digite 'menu' para voltar ao início."
                )
                user_states[phone_number] = 'initial' # Volta ao início
            elif '3' in message_lower or 'humano' in message_lower:
                response = "Entendido. Um dos nossos assistentes entrará em contacto consigo em breve. Obrigado!"
                # Aqui, você poderia adicionar uma lógica para notificar um funcionário
                user_states.pop(phone_number, None) # Termina a conversa do bot
            else:
                response = "Opção inválida. Por favor, escolha uma das opções: 1, 2 ou 3."

        # --- FLUXO DE AGENDAMENTO ---

        elif state == 'awaiting_patient_name':
            # Salva o nome e pede o motivo da consulta
            user_states[phone_number] = {
                'state': 'awaiting_reason',
                'patient_name': message_text
            }
            response = f"Obrigado, {message_text}. Qual é o motivo da consulta? (ex: Limpeza, Avaliação, Dor de dente)"

        elif state == 'awaiting_reason':
            # Salva o motivo e pede a data
            current_data = user_states.get(phone_number, {})
            current_data['state'] = 'awaiting_date'
            current_data['reason'] = message_text
            user_states[phone_number] = current_data
            response = "Entendido. Por favor, sugira uma data e hora para o agendamento (ex: 05/08/2025 às 15:00)."

        elif state == 'awaiting_date':
            # Salva a data e confirma tudo
            current_data = user_states.get(phone_number, {})
            patient_name = current_data.get('patient_name')
            reason = current_data.get('reason')
            appointment_datetime = message_text

            # Cria o agendamento no banco de dados
            new_appointment = Appointment(
                phone_number=phone_number,
                patient_name=patient_name,
                reason=reason,
                requested_datetime=appointment_datetime,
                status='pending' # Status inicial é pendente de confirmação
            )
            db.session.add(new_appointment)
            db.session.commit()

            response = (
                "Obrigado! O seu pedido de agendamento foi recebido e está pendente de confirmação.\n\n"
                f"👤 *Paciente:* {patient_name}\n"
                f"📋 *Motivo:* {reason}\n"
                f"🗓️ *Data Sugerida:* {appointment_datetime}\n\n"
                "Entraremos em contacto para confirmar o horário. Obrigado!"
            )
            user_states.pop(phone_number, None) # Termina a conversa

        # Comando para reiniciar a qualquer momento
        if 'menu' in message_lower and state != 'initial':
            user_states[phone_number] = 'initial'
            return self.process_message("menu", phone_number) # Chama a função novamente

        return response
