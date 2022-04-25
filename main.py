from db.dbClass import dbClass
from login.loginClass import loginClass
from funcionarios.funcionariosClass import funcionariosClass


# Mensagem de bem vindo ao sistema
print("Sistema de gestão de RH (v0.0.1)")
print("---------------------------------------------------")

# Cria a conexão com o banco de dados
dbClass = dbClass()
dbConn = dbClass.getDatabase()


# Cria o módulo de login
loginClass = loginClass(dbConn)

# Sistema de login
usuario = {}

while True:
    print("\nPor favor, faça login para continuar:")

    # TODO: O módulo de senha do grupo 1 deve entrar aqui na obtenção dos dados do usuário

    email = input("\t-> Email: ")
    senha = input("\t-> Senha: ")

    # Efetua a tentativa de login
    if loginClass.tryLogIn(email, senha):
        # Obtém o usuário logado
        usuario = loginClass.getUsuario()

        # Finaliza o loop
        print("\n---------------------------------------------------")
        break

    print("\tO email ou senha informados não é válido.")

	
# Se chegou até aqui, é por que o usuário efetuou o login com sucesso
print("Bem vindo(a) ao sistema, " + usuario["nome"] + "\n")

# Cria todos os módulos da aplicação
# Os novos módulos devem ser adicionados após essa linha
funcionariosClass = funcionariosClass(dbConn)

# Exibe os módulos e suas opções
# Os novos módulos devem ser adicionados nessa lista
opcoes = [{
    "number": 0,
    "descricao": funcionariosClass.getModuleDescription()
}, {
    "number": 9,
    "descricao": "Finalizar o programa"
}]

# Cria o array de opcoes com base no dicionário acima
opcoesNum = []

for opcao in opcoes:
    opcoesNum.append(opcao["number"])

# Itera para obter as opções
while True:
    print("Por favor, escolha uma opção:")

    # Exibe as opções disponíveis
    for opcao in opcoes:
        print("\t[" + str(opcao["number"]) + "] => " + opcao["descricao"])

    # Obtém a opção digitada
    opcaoSelecionada = -1

    # Se ocorrer algum erro no parse para int, opcaoSelecionada = -1
    try:
        opcaoSelecionada = int(input("\n> "))
    except:
        opcaoSelecionada = -1

    # Valida a opção selecionada
    if opcaoSelecionada not in opcoesNum:
        print("Opção não encontrada.\n")
        continue

    # Switch das opções
    if opcaoSelecionada == 0:
        funcionariosClass.showOptions(usuario["cargo"])

    else:
        exit(0)
