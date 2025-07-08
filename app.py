from flask import Flask
from database import db
from models import bcrypt
from routes.pacientes import pacientes_bp
from routes.medicos import medicos_bp
from routes.consultas import consultas_bp
from routes.prontuarios import prontuarios_bp
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager
from routes.routes_logs import logs_bp

app = Flask(__name__)

# Configuração do banco PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sghss.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração da chave secreta para JWT
app.config['JWT_SECRET_KEY'] = 'chave-secreta-supersegura'

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Registrar blueprints das rotas
app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(consultas_bp)
app.register_blueprint(prontuarios_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(logs_bp)


# Criar o banco na primeira execução
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "SGHSS Backend funcionando com PostgreSQL!"

if __name__ == '__main__':
    app.run(debug=True)
