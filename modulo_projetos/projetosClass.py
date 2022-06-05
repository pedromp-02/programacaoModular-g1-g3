from ast import dump
from flask import request
from flask_restful import Resource
from modulo_db.dbClass import dbClass
from modulo_login.loginClass import userModel
from bson.json_util import dumps, loads
from os import urandom

# Classe principal do módulo
class projetosClass(Resource):
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
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True:
				return {'message': 'Você não possui permissão para remover um projeto.'}, 401

			if not self.busca_projeto(id):
				return {'message': 'O projeto informado não foi encontrado.'}, 200

			self.db.projetos.delete_one({"_id": id})
			return {'message': 'Projeto removido com sucesso.'}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def get(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			# Se for para listar todos os projetos em andamento
			if id == 'list':
				# Verifica se o usuário possui permissão para visualizar os projetos
				if usuarioLogado["possuiPermissaoRH"] != True:
					return {'message': 'Você não possui permissão para visualizar os projetos em andamento.'}, 401

				return loads(dumps(list(self.db.projetos.find())))
			
			# Lista somente os projetos do usuário logado
			else:
				return loads(dumps(list(self.db.projetos.find({"participantes": {"$elemMatch": {"matricula": usuarioLogado["_id"]}}}))))
		
		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def put(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)
			
			# Verifica se o usuário está logado
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True:
				return {'message': 'Você não possui permissão para incluir um projeto.'}, 401

			if 'nome' not in request.json:
				return {'message': 'O nome do projeto é obrigatório.'}, 200

			if 'descricao' not in request.json:
				return {'message': 'A descrição do projeto é obrigatória.'}, 200

			if 'participantes' not in request.json:
				return {'message': 'Os participantes do projeto são obrigatórios.'}, 200

			id = urandom(5).hex()
			nome = request.json["nome"]
			descricao = request.json["descricao"]
			participantes = request.json["participantes"]

			self.db.projetos.insert_one({
				'_id': id,
				'nome': nome,
				'descricao': descricao,
				'participantes': participantes
			})

			return {'message': 'O projeto foi inserido com sucesso.', 'id': id}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def post(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True:
				return {'message': 'Você não possui permissão para atualizar um projeto.'}, 401

			if not self.busca_projeto(id):
				return {'message': 'O projeto informado não foi encontrado.'}, 200

			setObject = {}

			if 'nome' in request.json:
				setObject["nome"] = request.json["nome"]

			if 'descricao' in request.json:
				setObject["descricao"] = request.json["descricao"]

			if 'participantes' in request.json:
				setObject["participantes"] = request.json["participantes"]

			self.db.projetos.update_one(
				{"_id": id},
				{"$set": setObject}
			)

			return {'message': 'O projeto foi atualizado com sucesso.'}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	# Função responsável por verificar se o identificador de projeto existe
	def busca_projeto(self, id):
		for projeto in self.db.projetos.find():
			if (projeto['_id'] == id):
				return projeto

		return False