from os import urandom

# Classe principal do módulo
class projetosClass:
	# Armazena a conexão com o banco de dados
	db = {}

	# Número do cargo que possui permissão de acesso a esse módulo
	cargoNum = 9

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
	def showOptions(self, cargo):
		try:
			# Atualiza o cargo do usuário
			self.cargo = cargo

			if cargo == self.cargoNum:
				lista_op = ['Incluir um projeto', 'Excluir um projeto', 'Atualizar um projeto', 'Listar os projetos']
				
				while True:
					print("\n[MOD PROJETOS] - Por favor, escolha uma opção:")
					op = self.exibeOpcoesEPegaDigitada(lista_op)

					if op == 1:
						self.inclui()
					elif op == 2:
						self.remove()
					elif op == 3:
						self.atualiza()
					elif op == 4:
						self.lista()
					elif op == 9:
						return
				
			else:
				print('Você não tem permissão para tal ferramenta.')
	
		except Exception as ex:
			print("Ocorreu um erro na na função showOptions da classe projetosClass")
			print(ex)

	# Função responsável por verificar se um email de usuário já existe
	def busca_funcionario_email(self, email):
		try:
			for user in self.db.usuarios.find():
				if (user['email'] == email):
					return True
	
			return False

		except Exception as ex:
			print("Ocorreu um erro na na função showOptions da classe projetosClass")
			print(ex)

	# Função responsável por verificar se o identificador de projeto existe
	def busca_projeto(self, id):
		try:
			for projeto in self.db.projetos.find():
				if (projeto['_id'] == id):
					return projeto
	
			return False

		except Exception as ex:
			print("Ocorreu um erro na na função showOptions da classe projetosClass")
			print(ex)

	# Função responsável por incluir um projeto
	def inclui(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para incluir um novo projeto.")
				
				return
			
			id = urandom(5).hex()
			nome = input("Nome do projeto: ")
			descricao = input("Descrição do projeto: ")
			participantes = []

			# Obtém os participantes do projeto
			while True:
				email = input("Digite o email do funcionário a ser adicionado no projeto: ")

				if self.busca_funcionario_email(email):
					participantes.append(email)
				
				else:
					print("O email informado não é de nenhum funcionário")
					continue

				opcao = input("Deseja adicionar mais um participante (S, N): ")

				if opcao == 'S' or opcao == 's':
					continue

				break

			# Inclui o novo projeto no banco de dados
			self.db.projetos.insert_one({
				'_id': id,
	        	'nome': nome,
	        	'descricao': descricao,
	        	'participantes': participantes
	        })
	    	
			print('\nO projeto foi cadastrado com sucesso!\n')
			return

		except Exception as ex:
			print("Ocorreu um erro na na função inclui da classe funcionariosClass")
			print(ex)

	# Função responsável por remover um projeto
	def remove(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para remover um projeto.")
				return
		
			id = input("Digite o identificador do projeto que deseja excluir: ")
			projeto = self.busca_projeto(id)

			if projeto != False:
				self.db.projetos.delete_one({"_id": id})
				print('\Projeto removido com sucesso!\n')

				return
	
			print('\Projeto não encontrado!\n')

		except Exception as ex:
			print("Ocorreu um erro na na função remove da classe projetosClass")
			print(ex)

	# Função responsável por atualizar os dados de um usuário
	def atualiza(self):
		try:
			# Valida se o usuário logado possui permissão
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para atualizar um projeto.")
				return

			id = input("Digite o identificador do projeto que deseja excluir: ")
			projeto = self.busca_projeto(id)
			
			if projeto != False:
				texto = "Digite qual campo você deseja atualizar"
				campos = ["nome", "descricao", "participantes"]
				interface = ["Nome", "Descrição", "Participantes"]
	
				while True:
					print(texto)

					escolha = self.exibeOpcoesEPegaDigitada(interface)

					if escolha == 9:
						break

					if escolha != 3:
						atualizacao = input("Qual o novo valor do campo %s? "%campos[escolha-1])

						# Atualiza os dados
						self.db.projetos.update_one(
							{"_id": id},
							{"$set": {campos[escolha-1]: atualizacao}}
						)

					# Se for para atualizar os participantes
					else:
						participantes = projeto["participantes"]
						
						while True:
							email = input("Digite o email do participante. Caso ele já esteja no projeto, será removido. Caso contrário, será adicionado: ")

							if self.busca_funcionario_email(email):
								if email in participantes:
									participantes.remove(email)
								else:
									participantes.append(email)

								break
							
							else:
								print("O email informado não é de nenhum funcionário")
								continue

						# Atualiza os participantes do projeto
						self.db.projetos.update_one(
							{"_id": id},
							{"$set": {"participantes": participantes}}
						)
					
					print('\nAtualização feita com sucesso!\n')
				return
	
			print('\Projeto não encontrado!\n')

		except Exception as ex:
			print("Ocorreu um erro na na função atualiza da classe funcionariosClass")
			print(ex)

	# Função responsavel para mostar as opções de listagem de funcionários.
	def lista(self):
		try:
			if self.cargo != self.cargoNum:
				print("Você não possui permissão para visualizar os projetos.")
				return

			for projeto in self.db.projetos.find():
				print(f"\nIdentificador: {projeto['_id']}")
				print(f"Nome: {projeto['nome']}")
				print(f"Descrição: {projeto['descricao']}")
				print(f"Participantes:")

				for emailParticipante in projeto['participantes']:
					for usuarioParticipante in self.db.usuarios.find({'email': emailParticipante}):
						print(f"\t-> {usuarioParticipante['nome']} ({emailParticipante})")

				print('')
				print('-='*20)
					
		except Exception as ex:
			print("Ocorreu um erro na na função lista Funcionarios da classe funcionariosClass")
			print(ex)