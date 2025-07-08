from database import db
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

# ====================
# Usuário do sistema 
# ====================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    def verificar_senha(self, senha):
        return bcrypt.check_password_hash(self.senha_hash, senha)
# ====================
# Paciente 
# ====================
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)

# ====================
# Médico
# ====================
class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)

# ====================
# Consulta médica 
# ====================
class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    observacoes = db.Column(db.Text)
    is_teleconsulta = db.Column(db.Boolean, default=False)  

    paciente = db.relationship('Paciente', backref='consultas')
    medico = db.relationship('Medico', backref='consultas')

# ====================
# Prontuário 
# ====================
class Prontuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    anotacoes = db.Column(db.Text, nullable=False)

    paciente = db.relationship('Paciente', backref='prontuarios')
    medico = db.relationship('Medico', backref='prontuarios')
    
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(50), nullable=False)
    entidade = db.Column(db.String(50), nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    usuario = db.Column(db.String(80))
    data_hora = db.Column(db.DateTime, default=db.func.current_timestamp())
