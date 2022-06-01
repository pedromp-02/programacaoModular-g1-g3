from flask import Flask
from flask_restful import Api

from modulo_login.loginClass import loginClass
from modulo_projetos.projetosClass import projetosClass
from modulo_funcionarios.funcionariosClass import funcionariosClass

app = Flask(__name__)
api = Api(app)

# Adicionando as controladores a API
api.add_resource(loginClass, '/login')
api.add_resource(projetosClass, '/projetos/<id>')
api.add_resource(funcionariosClass, '/funcionarios/<id>')

if __name__ == '__main__':
    app.run()

# # Mensagem de bem vindo ao sistema
# print("Sistema de gestão de RH (v0.0.1)")
# print("---------------------------------------------------")

# # Cria a conexão com o banco de dados
# dbClass = dbClass()

# try:
#     dbConn = dbClass.getDatabase()

# except Exception as ex:
# 	print("Ocorreu um erro na na função getDatabase da classe dbClass")
# 	print(ex)
# 	exit()

# # Cria o módulo de login
# loginClass = loginClass(dbConn)

# # Sistema de login
# usuario = {}

# while True:
#     print("\nPor favor, faça login para continuar:")

#     # TODO: O módulo de senha do grupo 1 deve entrar aqui na obtenção dos dados do usuário

#     email = input("\t-> Email: ")
#     senha = getpass("\t-> Senha: ")

#     # Efetua a tentativa de login
#     if loginClass.tryLogIn(email, senha):
#         # Obtém o usuário logado
#         usuario = loginClass.getUsuario()

#         # Finaliza o loop
#         print("\n---------------------------------------------------")
#         break

#     print("\tO email ou senha informados não é válido.")

	
# # Se chegou até aqui, é por que o usuário efetuou o login com sucesso
# print("Bem vindo(a) ao sistema, " + usuario["nome"] + "\n")

# # Cria todos os módulos da aplicação
# # Os novos módulos devem ser adicionados após essa linha
# funcionariosClass = funcionariosClass(dbConn)
# projetosClass = projetosClass(dbConn)

# # Exibe os módulos e suas opções
# # Os novos módulos devem ser adicionados nessa lista
# opcoes = [{
#     "number": 1,
#     "descricao": funcionariosClass.getModuleDescription()
# }, {
#     "number": 2,
#     "descricao": projetosClass.getModuleDescription()
# }, {
#     "number": 9,
#     "descricao": "Finalizar o programa"
# }]

# # Cria o array de opcoes com base no dicionário acima
# opcoesNum = []

# for opcao in opcoes:
#     opcoesNum.append(opcao["number"])

# # Itera para obter as opções
# while True:
#     print("Por favor, escolha uma opção:")

#     # Exibe as opções disponíveis
#     for opcao in opcoes:
#         print("\t[" + str(opcao["number"]) + "] => " + opcao["descricao"])

#     # Obtém a opção digitada
#     opcaoSelecionada = -1

#     # Se ocorrer algum erro no parse para int, opcaoSelecionada = -1
#     try:
#         opcaoSelecionada = int(input("\n> "))
#     except:
#         opcaoSelecionada = -1

#     # Valida a opção selecionada
#     if opcaoSelecionada not in opcoesNum:
#         print("Opção não encontrada.\n")
#         continue

#     # Switch das opções
#     if opcaoSelecionada == 1:
#         funcionariosClass.showOptions(usuario["email"], usuario["cargo"])

#     elif opcaoSelecionada == 2:
#         projetosClass.showOptions(usuario["cargo"])

#     else:
#         exit()
