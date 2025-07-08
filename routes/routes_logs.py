from flask import Blueprint, jsonify
from models import Log
from flask_jwt_extended import jwt_required

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')

@logs_bp.route('', methods=['GET'])
@jwt_required()
def listar_logs():
    logs = Log.query.order_by(Log.data_hora.desc()).all()
    lista = [{
        'id': log.id,
        'usuario': log.usuario,
        'acao': log.acao,
        'entidade': log.entidade,
        'entidade_id': log.entidade_id,
        'timestamp': log.data_hora.isoformat() if log.data_hora else None
    } for log in logs]
    return jsonify(lista), 200
