# 🏥 SGHSS – Sistema de Gestão Hospitalar e de Serviços de Saúde

Este projeto é um sistema **Back-end** desenvolvido em **Python (Flask)** para gerenciar pacientes, médicos, consultas, prontuários e usuários. Ele inclui autenticação JWT e registros de logs de ações realizadas no sistema.

## 🚀 Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/index.html) (padrão, mas pode ser adaptado para PostgreSQL)
- [Postman](https://www.postman.com/) para testes

---

## 📁 Estrutura de Pastas

📦Trabalho_SGHSS
├── app.py
├── database.py
├── models.py
├── logs.py
├── routes/
│ ├── auth.py
│ ├── pacientes.py
│ ├── medicos.py
│ ├── consultas.py
│ ├── prontuarios.py
│ └── routes_logs.py
├── requirements.txt

yaml
Copiar
Editar

---

## ⚙️ Como Executar o Projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/k-Camila/Trabalho_SGHSS.git
cd Trabalho_SGHSS
Crie e ative um ambiente virtual (opcional, mas recomendado):

bash
Copiar
Editar
python -m venv venv
venv\Scripts\activate  # Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute a aplicação:

bash
Copiar
Editar
python app.py
A API estará disponível em: http://127.0.0.1:5000/

🔐 Autenticação
Use as rotas de login e registro para obter um token JWT:

Registro:
http
Copiar
Editar
POST /register
{
  "username": "admin",
  "senha": "123456",
  "tipo": "admin"
}
Login:
http
Copiar
Editar
POST /login
{
  "username": "admin",
  "senha": "123456"
}
O token JWT deve ser enviado no cabeçalho das requisições protegidas:
Authorization: Bearer <seu_token>

📌 Funcionalidades da API
👩‍⚕️ Médicos (/medicos)
GET /medicos — Listar todos

POST /medicos — Criar

GET /medicos/<id> — Buscar por ID

PUT /medicos/<id> — Atualizar

DELETE /medicos/<id> — Excluir

🧍 Pacientes (/pacientes)
Funcionalidade CRUD completa

📋 Consultas (/consultas)
Listar todas, listar teleconsultas e presenciais

Criar, editar e excluir

📁 Prontuários (/prontuarios)
CRUD de anotações clínicas por médicos

📄 Logs (/logs)
Visualização de todas as ações realizadas por usuários autenticados (CREATE, READ, UPDATE, DELETE)

✅ Testes com Postman
Você pode importar a coleção de testes no Postman com as rotas da API para:

Testar autenticação

Criar usuários

Realizar CRUD de todas as entidades

Visualizar logs

📌 Observações
Este projeto pode ser facilmente adaptado para PostgreSQL.

Para produção, substitua a JWT_SECRET_KEY e use variáveis de ambiente.

👩‍💻 Desenvolvido por
Camila Soares
GitHub
