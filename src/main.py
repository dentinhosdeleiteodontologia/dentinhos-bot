# main.py (para o serviço do bot)

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # Manter para a migração do DB, se necessário

# --- Configuração da Aplicação ---
app = Flask(__name__)

# Configuração de Banco de Dados
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-para-o-bot') # Uma chave secreta para o bot

# --- Inicialização das Extensões ---
db = SQLAlchemy(app)
migrate = Migrate(app, db) # Manter para a migração do DB, se necessário

# --- Modelos e Blueprints ---
# Importar apenas os modelos e blueprints necessários para o bot
from src.models.conversation import Conversation # O bot interage com conversas
# Não precisamos de User, Patient, Schedule aqui

from src.routes.whatsapp import whatsapp_bp # Apenas o blueprint do WhatsApp

# Registrar apenas o blueprint do WhatsApp
app.register_blueprint(whatsapp_bp)

# --- Criação do Banco de Dados (se necessário) ---
# Isto é importante para garantir que as tabelas do bot são criadas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
