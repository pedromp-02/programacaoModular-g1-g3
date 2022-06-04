from flask import request
from flask_restful import Resource
from modulo_db.dbClass import dbClass
from modulo_login.loginClass import userModel
from bson.json_util import dumps, loads
from os import urandom
import modulo_cripto

# Classe principal do módulo
class funcionariosClass(Resource):
	# Armazena a conexão com o banco de dados
	db = None

	def __init__(self):
		# Cria a conexão com o banco de dados
		try:
			self.db = dbClass.getDatabase()
		except Exception as ex:
			print(ex)
		
		super().__init__()

	def delete(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "cargo" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["cargo"] != 9 and usuarioLogado["id"] != id:
				return {'message': 'Você não possui permissão para remover um outro funcionário.'}, 401

			if not self.busca_funcionario(id):
				return {'message': 'O funcionário informado não foi encontrado.'}, 200

			self.db.usuarios.delete_one({"_id": id})
			return {'message': 'Funcionário removido com sucesso.'}, 200
		
		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def get(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "cargo" not in usuarioLogado:
				return usuarioLogado

			# Usuários com cargo diferente de 9 não podem visualizar outros funcionários
			if usuarioLogado["cargo"] != 9:
				# Se o id recebido for igual o id do usuário logado, retorna os dados dele
				if usuarioLogado["id"] == id:
					usuarios = self.db.usuarios.find({"_id": usuarioLogado["id"]}, {'senha': 0, 'salt': 0})

					for usuario in usuarios:
						return usuario, 200

				# Caso contrário, mensagem de erro
				return {'message': 'Você não possui permissão para visualizar dados de outros funcionários.'}, 401

			# Retorna a listagem dos funcionários
			return loads(dumps(list(self.db.usuarios.find({}, {'senha': 0, 'salt': 0}))))
		
		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500
  
	def put(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "cargo" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["cargo"] != 9:
				return {'message': 'Você não possui permissão para incluir um funcionário.'}, 401

			if 'nome' not in request.json:
				return {'message': 'O nome é obrigatório.'}, 200

			if 'email' not in request.json:
				return {'message': 'o email é obrigatório.'}, 200

			if 'usuario' not in request.json:
				return {'message': 'O usuário é obrigatório.'}, 200

			if 'senha' not in request.json:
				return {'message': 'A senha é obrigatória.'}, 200

			id = urandom(5).hex()
			nome = request.json["nome"]
			email = request.json["email"]
			usuario = request.json["usuario"]
			senha = request.json["senha"]

			# Gera o salt para o novo usuário
			salt = urandom(16).hex()

			# Criptografa a senha digitada pelo usuário
			senhaCriptografada = modulo_cripto.generate_hashed_password('sha256', senha, salt, 100, 64)

			self.db.usuarios.insert_one({
				'_id': id,
				'nome': nome,
				'email': email,
				'usuario': usuario,
				'senha': senhaCriptografada,
				'cargo': 1,
				'salt': salt
			})

			return {'message': 'O usuário foi inserido com sucesso.', 'id': id}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def post(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "cargo" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["cargo"] != 9 and usuarioLogado["id"] != id:
				return {'message': 'Você não possui permissão para alterar outro funcionário.'}, 401

			if not self.busca_funcionario(id):
				return {'message': 'O funcionário informado não foi encontrado.'}, 200

			setObject = {}

			if 'nome' in request.json:
				setObject["nome"] = request.json["nome"]

			if 'email' in request.json:
				setObject["email"] = request.json["email"]

			if 'usuario' in request.json:
				setObject["usuario"] = request.json["usuario"]

			if 'senha' in request.json:
				senha = request.json["senha"]

				# Gera o salt para a nova senha
				salt = urandom(16).hex()

				# Criptografa a senha digitada pelo usuário
				senhaCriptografada = modulo_cripto.generate_hashed_password('sha256', senha, salt, 100, 64)

				setObject["senha"] = senhaCriptografada
				setObject["salt"] = salt

			self.db.usuarios.update_one(
				{"_id": id},
				{"$set": setObject}
			)

			return {'message': 'O usuário foi atualizado com sucesso.'}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	# Função responsável por verificar se um email de usuário já existe, para não ter repetições de emails no DB.
	def busca_funcionario(self, id):
		for user in self.db.usuarios.find({'_id': id}):
			if user["_id"] == id:
				return True

		return False