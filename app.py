from flask import Flask
from flask_restful import Api

# Classe implementando o padrão singleton para ser reutilizado nos outros módulos e classes
class AppContext(object):
    _app = None
    _api = None

    # Não tem contrutor para a classe
    def __init__(self):
        exit()

    @classmethod
    def app(cls):
        if cls._app is None:
            cls._app = Flask(__name__)

        return cls._app

    @classmethod
    def api(cls):
        if cls._api is None:
            cls._api = Api(cls._app)

        return cls._api