import os
from flask import Blueprint, request, jsonify

whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route('/api/whatsapp/webhook', methods=['GET'])
def verify_webhook():
    print("\n[WEBHOOK GET] Recebida requisição GET para o webhook.")
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    print(f"[WEBHOOK GET] Mode: {mode}, Token: {token}, Challenge: {challenge}")

    if mode and token:
        if mode == 'subscribe' and token == os.environ.get('VERIFY_TOKEN'):
            print("[WEBHOOK GET] Webhook verificado com sucesso!")
            return challenge, 200
        else:
            print("[WEBHOOK GET] Falha na verificação: Token ou modo incorreto.")
            return jsonify({'status': 'Verification failed'}), 403
    else:
        print("[WEBHOOK GET] Falha na verificação: Parâmetros ausentes.")
        return jsonify({'status': 'Missing parameters'}), 400

@whatsapp_bp.route('/api/whatsapp/webhook', methods=['POST'])
def process_webhook():
    print("\n[WEBHOOK POST] Recebida requisição POST para o webhook.")
    data = request.get_json()
    print(f"[WEBHOOK POST] Dados recebidos: {data}")

    # Aqui você adicionaria a lógica para processar a mensagem
    # Por enquanto, apenas retornamos um 200 OK para o WhatsApp
    # para indicar que recebemos a mensagem.

    return jsonify({'status': 'OK'}), 200

