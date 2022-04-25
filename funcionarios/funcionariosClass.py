# Módulo do controle de funcionários
# Responsável por gerenciar todas as operações dos funcionários
#
# Criado em 21-04-2022 por Pedro Arduini e Gusthavo
# --------------------------------------------------------------------
# Atualizado em 22-04-2022 por Lucas Deano:
# Inclusão de tratamento de erros nas funções (try/catch)
# Inclusão do recebimento da classe de banco de dados
# Inclusão das funções getModuleDescription e showOptions
# Inclusão da validação do cargo do usuário ao executar uma função de manipulação de dados
# --------------------------------------------------------------------

# Classe principal do módulo
class funcionariosClass:
	# Armazena a conexão com o banco de dados
	db = {}

	# Armazena o cargo do cliente logado para fazer as validações nas funções de manipulação de dados
	clientCargo = None

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

	# Função responsável por exibir as opções do módulo
	# Exibida para: Todos
	def showOptions(self, cargo):
		try:
			# Atualiza o cargo do usuário
			self.cargo = cargo

			print("\n[MOD FUNCIONÁRIOS] - Por favor, escolha uma opção:")

			if cargo == self.cargoNum:
				lista_op = ['Incluir funcionario','Excluir funcionario','Atualizar funcionario','Voltar']
				
				
				while True:
					for i in range(4):
						print(f'\t[{i+1}] => {lista_op[i]} ')
						
					op = int(input('\n> '))
					if op < 1 or op >4:
						print('Opção não encontrada.\n')
						print('Por favor, escolha uma opção:')
						continue
					break

				
				if op == 1:
					self.inclui()
				elif op == 2:
					self.remove()
				elif op == 3:
					self.atualiza()
				elif op == 4:
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
			senha = input('Digite a senha do usuario: ')
			cargo = int(input('Digite o cargo do usuário: '))
	
			self.db.usuarios.insert_one({
	        	'nome': nome,
	        	'email': email,
	        	'usuario': usuario,
	        	'senha': senha,
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
				campos = ["nome","email","usuario","senha","cargo"]
				interface = ["1 - Nome", "2 - E-mail", "3 - Usuário", "4 - Senha", "5 - Cargo", "6 - Não quero atualizar mais nada"]
	
				while True:
					print(texto)
					
					for i in range(len(interface)):
						print(interface[i])
	
					escolha = int(input())
	
					if escolha == 6:
						break
					elif escolha > 6 or escolha <1:
						print('-='*20)
						print("Digite um campo valído!")
						print('-='*20)
					else:
						atualizacao = input("Qual o novo valor do campo %s? "%campos[escolha-1])

					# Atualiza os dados
					self.db.usuarios.update_one(
		                {"email": email},
		                {"$set": {campos[escolha-1]: atualizacao}}
		            )
					print('\nAtualização feita com sucesso!\n')
				return
	
			print('\nUsuário não encontrado!\n')

		except Exception as ex:
			print("Ocorreu um erro na na função atualiza da classe funcionariosClass")
			print(ex)


