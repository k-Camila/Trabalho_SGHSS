from flask import Blueprint, request, jsonify
from models import Consulta
from database import db
from flask_jwt_extended import jwt_required

consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')

# Listar todas as consultas ou por tipo (GET /consultas?tipo=teleconsulta)
@consultas_bp.route('', methods=['GET'])
@jwt_required()
def listar_consultas():
    tipo = request.args.get('tipo')

    if tipo == 'teleconsulta':
        consultas = Consulta.query.filter_by(is_teleconsulta=True).all()
    elif tipo == 'presencial':
        consultas = Consulta.query.filter_by(is_teleconsulta=False).all()
    else:
        consultas = Consulta.query.all()

    lista = []
    for c in consultas:
        lista.append({
            'id': c.id,
            'paciente_id': c.paciente_id,
            'medico_id': c.medico_id,
            'data': c.data,
            'hora': c.hora,
            'observacoes': c.observacoes,
            'is_teleconsulta': c.is_teleconsulta
        })
    return jsonify(lista), 200

# 🔹 Novo: Listar apenas teleconsultas (GET /consultas/teleconsultas)
@consultas_bp.route('/teleconsultas', methods=['GET'])
@jwt_required()
def listar_teleconsultas():
    consultas = Consulta.query.filter_by(is_teleconsulta=True).all()
    lista = []
    for c in consultas:
        lista.append({
            'id': c.id,
            'paciente_id': c.paciente_id,
            'medico_id': c.medico_id,
            'data': c.data,
            'hora': c.hora,
            'observacoes': c.observacoes,
            'is_teleconsulta': c.is_teleconsulta
        })
    return jsonify(lista), 200

# Criar uma nova consulta (POST /consultas)
@consultas_bp.route('', methods=['POST'])
@jwt_required()
def criar_consulta():
    data = request.get_json()

    nova_consulta = Consulta(
        paciente_id=data['paciente_id'],
        medico_id=data['medico_id'],
        data=data['data'],
        hora=data['hora'],
        observacoes=data.get('observacoes'),
        is_teleconsulta=data.get('is_teleconsulta', False)
    )
    db.session.add(nova_consulta)
    db.session.commit()
    return jsonify({'mensagem': 'Consulta cadastrada com sucesso!', 'id': nova_consulta.id}), 201

# Atualizar uma consulta existente (PUT /consultas/<id>)
@consultas_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_consulta(id):
    data = request.get_json()
    consulta = Consulta.query.get_or_404(id)

    consulta.paciente_id = data.get('paciente_id', consulta.paciente_id)
    consulta.medico_id = data.get('medico_id', consulta.medico_id)
    consulta.data = data.get('data', consulta.data)
    consulta.hora = data.get('hora', consulta.hora)
    consulta.observacoes = data.get('observacoes', consulta.observacoes)
    consulta.is_teleconsulta = data.get('is_teleconsulta', consulta.is_teleconsulta)

    db.session.commit()
    return jsonify({'mensagem': 'Consulta atualizada com sucesso!'}), 200

# Excluir consulta (DELETE /consultas/<int:id>)
@consultas_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({'mensagem': 'Consulta excluída com sucesso!'}), 200
