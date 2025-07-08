from models import Log
from database import db
from flask_jwt_extended import get_jwt_identity

def registrar_log(acao, entidade, entidade_id):
    usuario = get_jwt_identity()  # pega o usuário logado pelo JWT

    log = Log(
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id if entidade_id is not None else 0,
        usuario=usuario
        # data_hora será preenchido automaticamente pelo banco
    )
    db.session.add(log)
    db.session.commit()
