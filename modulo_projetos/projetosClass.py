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

	def isUserLogado(self):
		auth_header = request.headers.get('Authorization')

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

	def delete(self, id):
		cargoUsuarioLogado = self.isUserLogado()

		if cargoUsuarioLogado != 9:
			return {'message': 'Você não possui permissão para remover um projeto.'}, 401

		if not self.busca_projeto(id):
			return {'message': 'O projeto informado não foi encontrado.'}, 200

		self.db.projetos.delete_one({"_id": id})
		return {'message': 'Projeto removido com sucesso.'}, 200

	def get(self, id):
		cargoUsuarioLogado = self.isUserLogado()

		if cargoUsuarioLogado != 9:
			return {'message': 'Você não possui permissão para visualizar os projetos.'}, 401

		return loads(dumps(list(self.db.projetos.find())))

	def put(self, id):
		cargoUsuarioLogado = self.isUserLogado()

		if cargoUsuarioLogado != 9:
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

	def post(self, id):
		cargoUsuarioLogado = self.isUserLogado()

		if cargoUsuarioLogado != 9:
			return {'message': 'Você não possui permissão para atualizar um projeto.'}, 401

		if not self.busca_projeto(id):
			return {'message': 'O projeto informado não foi encontrado.'}, 200

		if 'nome' not in request.json:
			return {'message': 'O nome do projeto é obrigatório.'}, 200

		if 'descricao' not in request.json:
			return {'message': 'A descrição do projeto é obrigatória.'}, 200

		if 'participantes' not in request.json:
			return {'message': 'Os participantes do projeto são obrigatórios.'}, 200

		nome = request.json["nome"]
		descricao = request.json["descricao"]
		participantes = request.json["participantes"]

		self.db.projetos.update_one(
			{"_id": id},
			{"$set": 
				{
					"nome": nome,
					"descricao": descricao,
					"participantes": participantes
				}
			}
		)

		return {'message': 'O projeto foi atualizado com sucesso.'}, 200

	# Função responsável por verificar se o identificador de projeto existe
	def busca_projeto(self, id):
		try:
			for projeto in self.db.projetos.find():
				if (projeto['_id'] == id):
					return projeto
	
			return False

		except Exception as ex:
			return False