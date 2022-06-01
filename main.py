from flask import Flask
from flask_restful import Api

from modulo_login.loginClass import loginClass
from modulo_projetos.projetosClass import projetosClass
from modulo_funcionarios.funcionariosClass import funcionariosClass

app = Flask(__name__)
api = Api(app)

# Adicionando as controladores a API
api.add_resource(loginClass, '/login')
api.add_resource(projetosClass, '/projetos/<id>')
api.add_resource(funcionariosClass, '/funcionarios/<id>')

if __name__ == '__main__':
    app.run()