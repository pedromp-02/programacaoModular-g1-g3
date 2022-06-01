from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from modulo_login.loginClass import loginClass
from modulo_projetos.projetosClass import projetosClass
from modulo_funcionarios.funcionariosClass import funcionariosClass

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

# Adicionando as controladores a API
api.add_resource(loginClass, '/login')
api.add_resource(projetosClass, '/projetos/<id>')
api.add_resource(funcionariosClass, '/funcionarios/<id>')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='localhost', port=80)