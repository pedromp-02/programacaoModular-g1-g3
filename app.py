from flask import Flask
from flask_restful import Api
import random  
import string

# Classe implementando o padrão singleton para ser reutilizado nos outros módulos e classes
class AppContext(object):
    _app = None
    _api = None

    # TokenSecret é uma string de 16 caracteres aleatórios criada
    # a cada vez que a API é iniciada para que o token de uma sessão de outra versão
    # da API não seja válido na nova versão.
    _tokenSecret = None

    # Não tem contrutor para a classe
    def __init__(self):
        exit()

    @classmethod
    def app(cls):
        if cls._app is None:
            cls._app = Flask(__name__)
            cls._tokenSecret = ''.join((random.choice(string.ascii_lowercase) for x in range(16))) 

        return cls._app

    @classmethod
    def api(cls):
        if cls._api is None:
            cls._api = Api(cls._app)

        return cls._api

    @classmethod
    def getTokenSecret(cls):
        return cls._tokenSecret