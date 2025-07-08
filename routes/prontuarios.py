from flask import Blueprint, request, jsonify
from models import Prontuario
from database import db
from flask_jwt_extended import jwt_required

prontuarios_bp = Blueprint('prontuarios', __name__)

# Listar todos os prontuários (GET /prontuarios)
@prontuarios_bp.route('/prontuarios', methods=['GET'])
@jwt_required()
def listar_prontuarios():
    prontuarios = Prontuario.query.all()
    lista = [{
        'id': p.id,
        'paciente_id': p.paciente_id,
        'medico_id': p.medico_id,
        'data': p.data,
        'anotacoes': p.anotacoes
    } for p in prontuarios]
    return jsonify(lista), 200

# Buscar prontuário por ID (GET /prontuarios/<id>)
@prontuarios_bp.route('/prontuarios/<int:id>', methods=['GET'])
@jwt_required()
def buscar_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    return jsonify({
        'id': prontuario.id,
        'paciente_id': prontuario.paciente_id,
        'medico_id': prontuario.medico_id,
        'data': prontuario.data,
        'anotacoes': prontuario.anotacoes
    }), 200

# Criar novo prontuário (POST /prontuarios)
@prontuarios_bp.route('/prontuarios', methods=['POST'])
@jwt_required()
def criar_prontuario():
    data = request.get_json()
    novo_prontuario = Prontuario(
        paciente_id=data['paciente_id'],
        medico_id=data['medico_id'],
        data=data['data'],
        anotacoes=data['anotacoes']
    )
    db.session.add(novo_prontuario)
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário cadastrado com sucesso!'}), 201

# Atualizar prontuário (PUT /prontuarios/<id>)
@prontuarios_bp.route('/prontuarios/<int:id>', methods=['PUT'])
@jwt_required()
def editar_prontuario(id):
    data = request.get_json()
    prontuario = Prontuario.query.get_or_404(id)
    prontuario.paciente_id = data.get('paciente_id', prontuario.paciente_id)
    prontuario.medico_id = data.get('medico_id', prontuario.medico_id)
    prontuario.data = data.get('data', prontuario.data)
    prontuario.anotacoes = data.get('anotacoes', prontuario.anotacoes)
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário atualizado com sucesso!'}), 200

# Excluir prontuário (DELETE /prontuarios/<id>)
@prontuarios_bp.route('/prontuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    db.session.delete(prontuario)
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário excluído com sucesso!'}), 200
