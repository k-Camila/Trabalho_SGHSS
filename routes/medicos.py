from flask import Blueprint, request, jsonify
from models import Medico
from database import db
from flask_jwt_extended import jwt_required
from logs import registrar_log  # importa a função de registrar log

medicos_bp = Blueprint('medicos', __name__, url_prefix='/medicos')

# Listar médicos (GET /medicos)
@medicos_bp.route('', methods=['GET'])
@jwt_required()
def listar_medicos():
    medicos = Medico.query.all()
    lista = [{'id': m.id, 'nome': m.nome, 'especialidade': m.especialidade, 'crm': m.crm} for m in medicos]

    registrar_log('READ', 'medico', None)  # log para leitura/listagem, id None pois é vários registros

    return jsonify(lista), 200

# Buscar médico por ID (GET /medicos/<id>)
@medicos_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def buscar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({'erro': 'Médico não encontrado'}), 404

    registrar_log('READ', 'medico', id)  # log leitura de registro específico

    return jsonify({
        'id': medico.id,
        'nome': medico.nome,
        'especialidade': medico.especialidade,
        'crm': medico.crm
    }), 200

# Criar médico (POST /medicos)
@medicos_bp.route('', methods=['POST'])
@jwt_required()
def criar_medico():
    data = request.get_json()
    if not data.get('nome') or not data.get('especialidade') or not data.get('crm'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    if Medico.query.filter_by(crm=data['crm']).first():
        return jsonify({'erro': 'CRM já cadastrado'}), 409

    novo_medico = Medico(
        nome=data['nome'],
        especialidade=data['especialidade'],
        crm=data['crm']
    )
    db.session.add(novo_medico)
    db.session.commit()

    registrar_log('CREATE', 'medico', novo_medico.id)  # log criação

    return jsonify({'mensagem': 'Médico cadastrado com sucesso!', 'id': novo_medico.id}), 201

# Atualizar médico (PUT /medicos/<id>)
@medicos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({'erro': 'Médico não encontrado'}), 404

    data = request.get_json()
    medico.nome = data.get('nome', medico.nome)
    medico.especialidade = data.get('especialidade', medico.especialidade)

    crm_novo = data.get('crm')
    if crm_novo and crm_novo != medico.crm:
        if Medico.query.filter_by(crm=crm_novo).first():
            return jsonify({'erro': 'CRM já cadastrado'}), 409
        medico.crm = crm_novo

    db.session.commit()

    registrar_log('UPDATE', 'medico', id)  # log atualização

    return jsonify({'mensagem': 'Médico atualizado com sucesso!'}), 200

# Excluir médico (DELETE /medicos/<id>)
@medicos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({'erro': 'Médico não encontrado'}), 404

    db.session.delete(medico)
    db.session.commit()

    registrar_log('DELETE', 'medico', id)  # log exclusão

    return jsonify({'mensagem': 'Médico excluído com sucesso!'}), 200
