from app import AppContext
from flask_cors import CORS
from modulo_login.loginClass import loginClass
from modulo_projetos.projetosClass import projetosClass
from modulo_funcionarios.funcionariosClass import funcionariosClass

app = AppContext.app()
api = AppContext.api()

# Criando o CORS para o Client
cors = CORS(app, resources = {r"/api/*": {"origins": "*",}}, methods = ["GET", "POST", "PUT", "DELETE"], allow_headers = ["Content-Type", "Authorization"])

# Adicionando as controladores a API
api.add_resource(loginClass, '/api/login')
api.add_resource(projetosClass, '/api/projetos/<id>')
api.add_resource(funcionariosClass, '/api/funcionarios/<id>')

if __name__ == '__main__':
    app.run(host='localhost', port=80)