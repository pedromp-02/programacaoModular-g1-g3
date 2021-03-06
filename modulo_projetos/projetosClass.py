from ast import dump
from flask import request
from flask_restful import Resource
from sqlalchemy import func
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

				return self.getFuncionariosProjeto(self.db.projetos.find())
			
			# Lista somente os projetos do usuário logado
			else:
				return self.getFuncionariosProjeto(self.db.projetos.find({"participantes": {"$elemMatch": {"matricula": usuarioLogado["_id"]}}}))
		
		except Exception as ex:
			print(ex)
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

			if 'dataInicio' not in request.json:
				return {'message': 'A data de início do projeto é obrigatória.'}, 200

			if 'dataFim' not in request.json:
				return {'message': 'A data de término do projeto é obrigatória.'}, 200

			if 'participantes' not in request.json:
				return {'message': 'Os participantes do projeto são obrigatórios.'}, 200

			id = urandom(5).hex()
			nome = request.json["nome"]
			descricao = request.json["descricao"]
			dataInicio = request.json["dataInicio"]
			dataFim = request.json["dataFim"]
			participantes = request.json["participantes"]

			self.db.projetos.insert_one({
				'_id': id,
				'nome': nome,
				'descricao': descricao,
				'dataInicio': dataInicio,
				'dataFim': dataFim,
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

			if 'dataInicio' in request.json:
				setObject["dataInicio"] = request.json["dataInicio"]

			if 'dataFim' in request.json:
				setObject["dataFim"] = request.json["dataFim"]

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

	# Função responsável por obter os dados de cada funcionário que participam do projeto
	def getFuncionariosProjeto(self, projetos):
		projetosComFuncionarios = []

		for projeto in projetos:
			for funcionario in projeto["participantes"]:
				funcionarioData = self.getFuncionarioData(funcionario["matricula"])

				if funcionarioData != None:
					funcionario["nome"] = funcionarioData["nome"]
					funcionario["email"] = funcionarioData["email"]

			projetosComFuncionarios.append(projeto)

		return projetosComFuncionarios
	
	# Função responsável por obter os dados de um funcionário
	def getFuncionarioData(self, matricula):
		for funcionario in self.db.usuarios.find({"_id": matricula}):
			if (funcionario['_id'] == matricula):
				return funcionario

		return None