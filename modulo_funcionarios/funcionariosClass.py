from getpass import getpass
from os import urandom
import modulo_cripto

# Classe principal do módulo
class funcionariosClass:
	# Armazena a conexão com o banco de dados
	db = {}

	# Armazena o cargo do cliente logado para fazer as validações nas funções de manipulação de dados
	clientCargo = None

	# Armazena o email do cliente logado
	clientMail = None

	# Número do cargo que possui permissão de acesso a esse módulo
	cargoNum = 9

	# Função responsável por criar a classe. 
	# Atribui a conexão a uma variável local para ser usada no módulo
	def __init__(self, dbConn):
		try:
			self.db = dbConn
	
		except Exception as ex:
			print("Ocorreu um erro na na função __init__ da classe funcionariosClass")
			print(ex)

	# Função que retorna para a main a descrição do módulo
	def getModuleDescription(self):
		return "Controle de funcionários"

	# Função responsável por exibir uma lista de opções para o usuário
	def exibeOpcoesEPegaDigitada(self, listaDeOpcoes):
		for i in range(len(listaDeOpcoes)):
			print(f'\t[{i+1}] => {listaDeOpcoes[i]} ')

		print('\t[9] => Voltar')

		opcaoDigitada = int(input("\n> "))

		if opcaoDigitada == 9:
			return opcaoDigitada

		elif opcaoDigitada > len(listaDeOpcoes) or opcaoDigitada < 0:
			print('Opção não encontrada.\n')
			self.exibeOpcoesEPegaDigitada(listaDeOpcoes)

			return

		return opcaoDigitada

	# Função responsável por exibir as opções do módulo
	# Exibida para: Todos
	def showOptions(self, email, cargo):
		try:
			# Atualiza o email do usuário logado
			self.clientMail = email

			# Atualiza o cargo do usuário
			self.cargo = cargo

			if cargo == self.cargoNum:
				lista_op = ['Incluir funcionario', 'Excluir funcionario', 'Atualizar funcionario', 'Listar Funcionarios']
				
				while True:
					print("\n[MOD FUNCIONÁRIOS] - Por favor, escolha uma opção:")
					op = self.exibeOpcoesEPegaDigitada(lista_op)

					if op == 1:
						self.inclui()
					elif op == 2:
						self.remove()
					elif op == 3:
						self.atualiza()
					elif op == 4:
						self.showOpListaFuncionarios()
					elif op == 9:
						return
				
			else:
				print('Você não tem permissão para tal ferramenta.')
	
		except Exception as ex:
			print("Ocorreu um erro na na função showOptions da classe funcionariosClass")
			print(ex)

	# Função responsável por verificar se um email de usuário já existe, para não ter repetições de emails no DB.
	def busca_funcionario_email(self, email):
		try:
			for user in self.db.usuarios.find():
				if (user['email'] == email):
					return True
	
			return False

		except Exception as ex:
			print("Ocorreu um erro na na função showOptions da classe funcionariosClass")
			print(ex)
  
	# Função responsável por incluir um funcionário
	def inclui(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para incluir um novo funcionário.")
				
				return
			nome = input('Digite o nome do funcionario: ')
			
			while True:
				email = input('Digite o email do funcionario: ')
				
				if self.busca_funcionario_email(email):
					print('-='*20)
					print('Email já existente!')
					print('-='*20)
				else:
					break
	
			usuario = input('Digite o usuario: ')
			senha = getpass('Digite a senha do usuario: ')
			cargo = int(input('Digite o cargo do usuário: '))

			# Gera o salt para o novo usuário
			salt = urandom(16).hex()

			# Criptografa a senha digitada pelo usuário
			senhaCriptografada = modulo_cripto.generate_hashed_password('sha256', senha, salt, 100, 64)

			# Inclui o novo usuário no banco de dados
			self.db.usuarios.insert_one({
	        	'nome': nome,
	        	'email': email,
	        	'usuario': usuario,
	        	'senha': senhaCriptografada,
				'salt': salt,
	        	'cargo': cargo
	        })
	    	
			print('\nO usuário foi cadastrado com sucesso!\n')
			return

		except Exception as ex:
			print("Ocorreu um erro na na função inclui da classe funcionariosClass")
			print(ex)

	# Função responsável por remover um usuário
	def remove(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para remover um funcionário.")
				return
		
			email = input("Digite o e-mail do funcionário que deseja excluir: ")

			if email == self.clientMail:
				print("Você não possui permissão para remover você mesmo.")
				return
			
			if self.busca_funcionario_email(email):
				self.db.usuarios.delete_one({"email": email})
				print('\nUsuário removido com sucesso!\n')

				return
	
			print('\nUsuário não encontrado!\n')

		except Exception as ex:
			print("Ocorreu um erro na na função remove da classe funcionariosClass")
			print(ex)

	# Função responsável por atualizar os dados de um usuário
	def atualiza(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para atualizar um funcionário.")
				return

			email = input("Digite o email do funcionário que deseja atualizar: ")
			
			if self.busca_funcionario_email(email):
				texto = "Digite qual campo você deseja atualizar"
				campos = ["nome", "email", "usuario", "senha", "cargo"]
				interface = ["Nome", "E-mail", "Usuário", "Senha", "Cargo"]
	
				while True:
					print(texto)

					escolha = self.exibeOpcoesEPegaDigitada(interface)

					if escolha == 9:
						break

					if escolha != 4:
						atualizacao = input("Qual o novo valor do campo %s? "%campos[escolha-1])

						# Atualiza os dados
						self.db.usuarios.update_one(
							{"email": email},
							{"$set": {campos[escolha-1]: atualizacao}}
						)

					# Se for para atualizar a senha
					else:
						senha = getpass('Digite a nova senha do usuario: ')
						senhaConfirmacao = getpass('Confirme a nova senha do usuario: ')

						# Valida se as senhas digitadas são iguais
						if senha != senhaConfirmacao:
							print("As confirmação da senha falhou, tente novamente.")
							continue

						# Gera o salt para o novo usuário
						salt = urandom(16).hex()

						# Criptografa a senha digitada pelo usuário
						senhaCriptografada = modulo_cripto.generate_hashed_password('sha256', senha, salt, 100, 64)

						# Atualiza a senha
						self.db.usuarios.update_one(
							{"email": email},
							{"$set": 
								{
									"senha": senhaCriptografada,
									"salt": salt
								}
							}
						)
					
					print('\nAtualização feita com sucesso!\n')
				return
	
			print('\nUsuário não encontrado!\n')

		except Exception as ex:
			print("Ocorreu um erro na na função atualiza da classe funcionariosClass")
			print(ex)

	# Função responsavel para listar dados de um funcionario através do email
	def listaUm_email(self,email):
		try:
			for user in self.db.usuarios.find():
				
				if user['email'] == email:
					print('-='*20)
					print(f"Nome: {user['nome']}\nEmail: {user['email']}\nUsuario:{user['usuario']}\nCargo:{user['cargo']}")
					print('-='*20)

		
		except Exception as ex:
			print("Ocorreu um erro na na função listaUm_email da classe funcionariosClass")
			print(ex)

	# Função responsavel para listar dados dos funcionarios através do cargo (Lista todos os funcionário de cargo x)
	def listaPorCargo(self,cargo):
		try:	
			print('-='*20)

			for user in self.db.usuarios.find():				
				if int(user['cargo']) == cargo:
					print(f"Nome: {user['nome']}\nEmail: {user['email']}\nUsuario:{user['usuario']}\nCargo:{user['cargo']}")
					print('-='*20)
					
		except Exception as ex:
			print("Ocorreu um erro na na função listaPorCargo da classe funcionariosClass")
			print(ex)

	# Função responsavel por listar todos os funcionarios.
	def listaTodos(self):
		try:
			print('-='*20)

			for user in self.db.usuarios.find():
				print(f"Nome: {user['nome']}\nEmail: {user['email']}\nUsuario:{user['usuario']}\nCargo:{user['cargo']}")
				print('-='*20)
		
		except Exception as ex:
			print("Ocorreu um erro na na função listaTodos da classe funcionariosClass")
			print(ex)
	
	# Função responsavel para mostar as opções de listagem de funcionários.
	def showOpListaFuncionarios(self):
		try:
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para visualizar os funcionário.")
				return

			opcoes = ['Listar dados de um funcionario',
				 	'Listar dados dos funcionarios através do cargo','Listar todos os funcionarios','Voltar']

			while True:
				print("\n[MOD FUNCIONÁRIOS] - Por favor, escolha uma opção:")
				for i in range(4):
					print(f'\t[{i+1}] => {opcoes[i]} ')
				op_escolhida = int(input('\n> '))

				if op_escolhida < 1 or op_escolhida > 4:
					print('Opção não encontrada.\n')
					continue
					
				if op_escolhida == 1:
					email = input('Digite o email do funcionario: ')
					if self.busca_funcionario_email(email):
						self.listaUm_email(email)
					else:
						print('Usuario não encontrado.\n')
						
				elif op_escolhida == 2:
					cargo = int(input('Digite o cargo: '))
					self.listaPorCargo(cargo)
					
				elif op_escolhida == 3:
					self.listaTodos()
					
				elif op_escolhida == 4:
					return
					
		except Exception as ex:
			print("Ocorreu um erro na na função lista Funcionarios da classe funcionariosClass")
			print(ex)
