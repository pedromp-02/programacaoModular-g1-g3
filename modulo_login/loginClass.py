from flask import request
from flask_restful import Resource
from modulo_db.dbClass import dbClass
import modulo_cripto
import datetime
import jwt

class userModel():
    @staticmethod
    def encode_auth_token(cargo):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': cargo
            }

            return jwt.encode(payload, 'TOKEN_SECRETO', algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, 'TOKEN_SECRETO')
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'

        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

# Classe principal do módulo
class loginClass(Resource):
	# Armazena a conexão com o banco de dados
	db = None

	def __init__(self):
		# Cria a conexão com o banco de dados
		try:
			self.db = dbClass.getDatabase()
		except Exception as ex:
			print(ex)
		
		super().__init__()

	def post(self):
		if self.db == None:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

		if 'email' not in request.json:
			return {'message': 'O e-mail é obrigatório.'}, 200

		if 'senha' not in request.json:
			return {'message': 'A senha é obrigatória.'}, 200

		email = request.json["email"]
		senha = request.json["senha"]

		# Realiza a busca do usuário
		usuarios = self.db.usuarios.find({"email": email}).limit(1)

		# Se retornar uma quantidade de usuários diferente de 1, loguin falhou
		for usuario in usuarios:
			# Obtém os dados para verificar a senha
			senhaUsuarioNoBanco = usuario["senha"]
			saltUsuarioNoBanco = usuario["salt"]

			# Criptografa a senha digitada pelo usuário
			senhaCriptografada = modulo_cripto.generate_hashed_password('sha256', senha, saltUsuarioNoBanco, 100, 64)

			# Se senhas forem diferentes
			if senhaUsuarioNoBanco != senhaCriptografada:
				return {'message': 'As credenciais de acesso não são válidas.'}, 401

			# Se as senhas forem iguais, remove a senha e o salt do objeto
			else:
				usuario.pop("senha")
				usuario.pop("salt")

			# Gera o token de autenticação
			auth_token = userModel.encode_auth_token(usuario["cargo"])
			response = {
				'message': 'OK.',
				'auth': auth_token
			}

			return response, 200
		
		return {'message': 'As credenciais de acesso não são válidas.'}, 401
