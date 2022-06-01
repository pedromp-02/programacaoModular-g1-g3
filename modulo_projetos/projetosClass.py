# Classe principal do módulo
class projetosClass:
	# Armazena a conexão com o banco de dados
	db = {}

	# Função responsável por criar a classe. 
	# Atribui a conexão a uma variável local para ser usada no módulo
	def __init__(self, dbConn):
		try:
			self.db = dbConn
	
		except Exception as ex:
			print("Ocorreu um erro na na função __init__ da classe projetosClass")
			print(ex)

	# Função que retorna para a main a descrição do módulo
	def getModuleDescription(self):
		return "Controle dos projetos"