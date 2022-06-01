import modulo_cripto

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
			# Realiza a busca do usuário
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
					return False

				# Se as senhas forem iguais, remove a senha e o salt do objeto
				else:
					usuario.pop("senha")
					usuario.pop("salt")

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