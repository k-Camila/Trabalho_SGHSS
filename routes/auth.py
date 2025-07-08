from flask import Blueprint, request, jsonify
from models import Usuario
from database import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'username' not in data or 'senha' not in data or 'tipo' not in data:
        return jsonify({'erro': 'Dados incompletos. Envie username, senha e tipo.'}), 400

    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'erro': 'Usuário já existe'}), 409

    novo_usuario = Usuario(username=data['username'], tipo=data['tipo'])
    novo_usuario.set_senha(data['senha'])

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'senha' not in data:
        return jsonify({'erro': 'Dados incompletos'}), 400

    usuario = Usuario.query.filter_by(username=data['username']).first()

    if not usuario or not usuario.verificar_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    token = create_access_token(identity=usuario.username, expires_delta=timedelta(hours=2))
    return jsonify({'token': token}), 200