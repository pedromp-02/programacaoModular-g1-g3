from flask import request
from flask_restful import Resource
from modulo_db.dbClass import dbClass
from app import AppContext
import modulo_cripto
import datetime
import jwt

# Classe que gera o token de autenticação e valida o mesmo
class userModel():
	@staticmethod
	def encode_auth_token(user):
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
				'sub': user
			}

			return jwt.encode(payload, AppContext.getTokenSecret(), algorithm="HS256")

		except Exception as e:
			print(e)
			return None

	@staticmethod
	def decode_auth_token(auth_token):
		try:
			return jwt.decode(auth_token, AppContext.getTokenSecret(), algorithms=["HS256"])

		except Exception as e:
			return 'Token inválido. Faça login novamente.'

	@staticmethod
	def isUserLogado(req):
		auth_header = req.headers.get('Authorization')

		if auth_header:
			auth_token = auth_header.split(" ")[1]
		else:
			auth_token = ''

		if auth_token:
			resp = userModel.decode_auth_token(auth_token)

			if isinstance(resp, str):
				return {'message': resp}, 401

			return resp["sub"]
			
		return {'message': 'O Token é obrigatório'}, 401


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
		try:
			if self.db == None:
				return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

			if 'email' not in request.json:
				return {'message': 'O e-mail é obrigatório.'}, 200

			if 'senha' not in request.json:
				return {'message': 'A senha é obrigatória.'}, 200

			email = request.json["email"]
			senha = request.json["senha"]

			# Realiza a busca do 'usuário
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
				auth_token = userModel.encode_auth_token(usuario)

				if auth_token == None:
					return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

				# Cria a resposta
				response = {
					'auth': auth_token,
					'user': usuario
				}

				return response, 200
		
			return {'message': 'As credenciais de acesso não são válidas.'}, 401

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500
