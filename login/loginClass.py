# Módulo de login
# Responsável por efetuar o login e retornar os dados do usuário
#
# Criado em 21-04-2022 por Pedro Arduini e Gusthavo
# --------------------------------------------------------------------

# Classe principal do módulo
class loginClass:
	# Armazena a conexão com o banco de dados
	db = {}

	# Armazena os dados do usuário logado
	usuario = {}

	def __init__(self, dbConn):
		try:
			self.db = dbConn
	
		except Exception as ex:
			print("Ocorreu um erro na na função __init__ da classe loginClass")
			print(ex)

	# Função responsável por efetuar a tentativa de login
	def tryLogIn(self, email, senha):
		try:
			# Realiza a busca do usuário e remove o campo senha do retorno, pois é um dado sensível
			usuarios = self.db.usuarios.find({"email": email,
				"senha": senha},{"senha": 0}).limit(1)

			# Retorna true ou false de acordo com o array
			for usuario in usuarios:
				# Guarda os dados do usuário logado
				self.usuario = usuario
				return True
			
			return False
	
		except Exception as ex:
			print("Ocorreu um erro na na função tryLogIn da classe loginClass")
			print(ex)

	# Função responsável por retornar o usuário logado
	def getUsuario(self):
		try:
			return self.usuario

		except Exception as ex:
			print("Ocorreu um erro na na função getUsuario da classe loginClass")
			print(ex)