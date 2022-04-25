import pymongo
import os

# Módulo do banco de dados
# Responsável por gerenciar todas as requisições para o banco
#
# Criado em 05-04-2022 por Lucas Deano
# --------------------------------------------------------------------

# Classe principal do módulo
class dbClass:
	strConn = ""

	# Função de construção da classe do módulo
	# Responsável por criar a string de conexão com o servidor do mongo
	def __init__(self):
		try:
			strConn = "mongodb+srv://<username>:<password>@<server>?<params>"

			# Adicionando dados a string de conexão
			strConn = strConn.replace("<username>", os.environ['strConnUsername'])
			strConn = strConn.replace("<password>", os.environ['strConnPassword'])
			strConn = strConn.replace("<server>", os.environ['strConnServer'])
			strConn = strConn.replace("<params>", os.environ['strConnParams'])

			# Atualiza a string de conexão na classe
			self.strConn = strConn
		
		except Exception as ex:
			print("Ocorreu um erro na na função __init__ da classe dbClass")
			print(ex)

	# Função responsável por retornar a conexão com o banco de dados
	def getDatabase(self):
		try:
			# Cria a conexão com o banco
			client = pymongo.MongoClient(self.strConn, serverSelectionTimeoutMS=5000)

			# Retorna o banco correto
			return client["TrabalhoProgModular"]
		
		except Exception as ex:
			print("Ocorreu um erro na na função getDatabase da classe dbClass")
			print(ex)
		