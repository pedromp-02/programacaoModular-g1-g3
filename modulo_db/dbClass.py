import pymongo

# Classe principal do módulo
class dbClass:
	# Função responsável por retornar a conexão com o banco de dados
	def getDatabase():
		strConn = "mongodb+srv://<username>:<password>@<server>?<params>"

		# Adicionando dados a string de conexão
		strConn = strConn.replace("<username>", "deanolucas")
		strConn = strConn.replace("<password>", "2RayOVKrVCA6lyTv")
		strConn = strConn.replace("<server>", "cluster0.9bqok.mongodb.net/myFirstDatabase")
		strConn = strConn.replace("<params>", "retryWrites=true&w=majority")
	
		# Cria a conexão com o banco
		client = pymongo.MongoClient(strConn, serverSelectionTimeoutMS=5000)

		# Retorna o banco correto
		return client["TrabalhoProgModular"]
		