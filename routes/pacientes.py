from flask import Blueprint, request, jsonify
from models import Paciente
from database import db
from flask_jwt_extended import jwt_required
from logs import registrar_log  # Importa o logger

pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

# Criar paciente (POST /pacientes)
@pacientes_bp.route('', methods=['POST'])
@jwt_required()
def criar_paciente():
    data = request.get_json()
    if not data.get('nome') or not data.get('cpf') or not data.get('idade') or not data.get('sexo'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    if Paciente.query.filter_by(cpf=data['cpf']).first():
        return jsonify({'erro': 'CPF já cadastrado'}), 409

    paciente = Paciente(
        nome=data['nome'],
        cpf=data['cpf'],
        idade=data['idade'],
        sexo=data['sexo']
    )
    db.session.add(paciente)
    db.session.commit()

    registrar_log('CREATE', 'paciente', paciente.id)  # log criação

    return jsonify({'mensagem': 'Paciente criado', 'id': paciente.id}), 201

# Listar pacientes (GET /pacientes)
@pacientes_bp.route('', methods=['GET'])
@jwt_required()
def listar_pacientes():
    pacientes = Paciente.query.all()
    lista = []
    for p in pacientes:
        lista.append({
            'id': p.id,
            'nome': p.nome,
            'cpf': p.cpf,
            'idade': p.idade,
            'sexo': p.sexo
        })

    registrar_log('READ', 'paciente', None)  # log listagem geral

    return jsonify(lista), 200

# Buscar paciente por ID (GET /pacientes/<int:id>)
@pacientes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def buscar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

    registrar_log('READ', 'paciente', id)  # log leitura de um registro

    return jsonify({
        'id': paciente.id,
        'nome': paciente.nome,
        'cpf': paciente.cpf,
        'idade': paciente.idade,
        'sexo': paciente.sexo
    }), 200

# Atualizar paciente (PUT /pacientes/<int:id>)
@pacientes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

    data = request.get_json()
    paciente.nome = data.get('nome', paciente.nome)
    paciente.idade = data.get('idade', paciente.idade)
    paciente.sexo = data.get('sexo', paciente.sexo)

    cpf_novo = data.get('cpf')
    if cpf_novo and cpf_novo != paciente.cpf:
        if Paciente.query.filter_by(cpf=cpf_novo).first():
            return jsonify({'erro': 'CPF já cadastrado'}), 409
        paciente.cpf = cpf_novo

    db.session.commit()

    registrar_log('UPDATE', 'paciente', id)  # log atualização

    return jsonify({'mensagem': 'Paciente atualizado'}), 200

# Excluir paciente (DELETE /pacientes/<int:id>)
@pacientes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({'erro': 'Paciente não encontrado'}), 404

    db.session.delete(paciente)
    db.session.commit()

    registrar_log('DELETE', 'paciente', id)  # log exclusão

    return jsonify({'mensagem': 'Paciente excluído'}), 200
