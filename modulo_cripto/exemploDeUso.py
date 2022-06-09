import modulo_cripto
import random
import string


  
password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10)) #senha digitada pelo usuario no cadastro
truepassword = password #senha digitada pelo usuario no login corretamente
falsepassword = password + 'a' #senha digitada pelo usuario no login de forma errada
type = 'sha256' 
iterations = 100
iterations_test = 99
dklen = 64
salt1 =  "b70c4693d1d8d802971c154e731eb544" # grupo 1 cria salt com 32 caracteres
salt2 =  "9a1ff6597127ae6e485cc1ff6a118fc7" #grupo 1 cria salt com 32 caracteres



def testasenhacorreta():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) == modulo_cripto.generate_hashed_password(type, truepassword,salt1,iterations,dklen)
 
print(f"Testa se a senha correta digitada no login (truepassword = {password}) corresponde a senha que o usuário criou no cadastro (password = {password}). Se não houver erro o teste foi bem-sucedido")

try:
  testasenhacorreta()
  print("Resultado: successo")
except:
  print("Resultado: falha")

  #troquei
  
def testasenhaerrada():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) == modulo_cripto.generate_hashed_password(type, falsepassword,salt1,iterations,dklen)

print(f"Testa se a senha errada digitada no login (falsepassword = {falsepassword}) NÃO corresponde a senha que o usuário criou no cadastro (password = {password}). Se não houver erro o teste foi bem-sucedido")
try:
  testasenhaerrada()
  print("Resultado: successo")
except:
  print("Resultado: falha")

def testasaltsdiferentes():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) != modulo_cripto.generate_hashed_password(type, password,salt2,iterations,dklen)

print(f"Testa se a função retorna valores distintos para os mesmos parâmetros apenas com salts (salt1 = {salt1}, salt2 = {salt2}) diferentes" )
try:
  testasaltsdiferentes()
  print("Resultado: sucesso")
except:
  print("Resultado: falha")
  
def testaiterationsdiferentes():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) != modulo_cripto.generate_hashed_password(type, password,salt1,iterations_test,dklen)

print(f"Testa se a função retorna valores distintos para os mesmos parâmetros apenas com iterações (iterations = {iterations}, iterations_test = {iterations_test}) diferentes" )
try:
  testaiterationsdiferentes()
  print("Resultado: sucesso")
except:
  print("Resultado: falha")
