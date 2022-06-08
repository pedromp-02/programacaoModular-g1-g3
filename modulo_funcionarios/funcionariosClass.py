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
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True and usuarioLogado["_id"] != id:
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
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			# Usuários sem permissao do RH não podem visualizar outros funcionários
			if usuarioLogado["possuiPermissaoRH"] != True:
				# Se o id recebido for igual o id do usuário logado, retorna os dados dele
				if usuarioLogado["_id"] == id:
					usuarios = self.db.usuarios.find({"_id": usuarioLogado["_id"]}, {'senha': 0, 'salt': 0})

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
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True:
				return {'message': 'Você não possui permissão para incluir um funcionário.'}, 401

			if 'email' not in request.json:
				return {'message': 'o email é obrigatório.'}, 200

			# Verifica se o usuário já está cadastrado
			if self.busca_funcionario_dado(request.json["email"], 'email'):
				return {'message': 'O funcionário informado já está cadastrado.'}, 200

			if self.busca_funcionario_dado(request.json["cpf"], 'cpf'):
				return {'message': 'O funcionário informado já está cadastrado.'}, 200

			if 'nome' not in request.json:
				return {'message': 'O nome é obrigatório.'}, 200

			if 'usuario' not in request.json:
				return {'message': 'O usuário é obrigatório.'}, 200

			if 'senha' not in request.json:
				return {'message': 'A senha é obrigatória.'}, 200

			if 'cargo' not in request.json:
				return {'message': 'O cargo é obrigatório.'}, 200

			if 'salario' not in request.json:
				return {'message': 'O salário é obrigatório.'}, 200

			if 'dataAdmissao' not in request.json:
				return {'message': 'A data de admissão é obrigatória.'}, 200

			if 'dataNascimento' not in request.json:
				return {'message': 'A data de nascimento é obrigatória.'}, 200

			if 'cpf' not in request.json:
				return {'message': 'O CPF é obrigatório.'}, 200

			if 'endereco' not in request.json:
				return {'message': 'O endereço é obrigatório.'}, 200

			if 'dependentes' not in request.json:
				return {'message': 'Os dependentes são obrigatório.'}, 200

			id = urandom(5).hex()
			nome = request.json["nome"]
			email = request.json["email"]
			usuario = request.json["usuario"]
			senha = request.json["senha"]
			cargo = request.json["cargo"]
			salario = request.json["salario"]
			dataAdmissao = request.json["dataAdmissao"]
			dataNascimento = request.json["dataNascimento"]
			cpf = request.json["cpf"]
			endereco = request.json["endereco"]
			dependentes = request.json["dependentes"]

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
				'salt': salt,
				'cargo': cargo,
				'salario': salario,
				'dataAdmissao': dataAdmissao,
				'dataNascimento': dataNascimento,
				'cpf': cpf,
				'endereco': endereco,
				'dependentes': dependentes,
				'possuiPermissaoRH': False,
			})

			return {'message': 'O usuário foi inserido com sucesso.', 'id': id}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	def post(self, id):
		try:
			usuarioLogado = userModel.isUserLogado(request)

			# Verifica se o usuário está logado
			if "possuiPermissaoRH" not in usuarioLogado:
				return usuarioLogado

			if usuarioLogado["possuiPermissaoRH"] != True and usuarioLogado["_id"] != id:
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

			if 'cargo' in request.json:
				setObject["cargo"] = request.json["cargo"]

			if 'salario' in request.json:
				setObject["salario"] = request.json["salario"]

			if 'dataAdmissao' in request.json:
				setObject["dataAdmissao"] = request.json["dataAdmissao"]

			if 'dataNascimento' in request.json:
				setObject["dataNascimento"] = request.json["dataNascimento"]

			if 'cpf' in request.json:
				setObject["cpf"] = request.json["cpf"]

			if 'endereco' in request.json:
				setObject["endereco"] = request.json["endereco"]

			if 'dependentes' in request.json:
				setObject["dependentes"] = request.json["dependentes"]

			self.db.usuarios.update_one(
				{"_id": id},
				{"$set": setObject}
			)

			return {'message': 'O usuário foi atualizado com sucesso.'}, 200

		except Exception as ex:
			return {'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, 500

	# Função responsável por verificar se um email de usuário já existe, para não ter repetições de emails no DB.
	def busca_funcionario_dado(self, email, dado):
		for user in self.db.usuarios.find({dado: email}):
			if user[dado] == email:
				return True

		return False
	
	def busca_funcionario(self, id):
		for user in self.db.usuarios.find({'_id': id}):
			if user["_id"] == id:
				return True

		return False