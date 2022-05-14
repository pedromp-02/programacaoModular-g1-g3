import modulo_cripto
import random
import string
from os import urandom

def generate_salt():
    return urandom(16).hex()

  
password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10)) #senha digitada pelo usuario no cadastro (pode pegar direto em um teste do banco se quisef)
truepassword = password #senha digitada pelo usuario no login corretamente
falsepassword = password + 'a' #senha digitada pelo usuario no login de forma errada 
type = 'sha256' #tipo que o grupo 3 vai usar (eu acho)
iterations = 100 #tipo que o grupo 3 vai usar (eu acho)
dklen = 64 #tipo que o grupo 3 vai usar (eu acho)
salt1 = modulo_cripto.generate_salt() # grupo 1 cria salt com 32 caracteres (se quiser pode deixar ja no banco de dados um de teste e usar ele)
salt2 = modulo_cripto.generate_salt() #grupo 1 cria salt com 32 caracteres


def testasalt():
  assert salt1 != salt2






def testasenhacorreta():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) == modulo_cripto.generate_hashed_password(type, truepassword,salt1,iterations,dklen)
  



def testasenhaerrada():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) != modulo_cripto.generate_hashed_password(type, falsepassword,salt1,iterations,dklen)




def testasaltsdiferentes():
  assert modulo_cripto.generate_hashed_password(type, password,salt1,iterations,dklen) != modulo_cripto.generate_hashed_password(type, password,salt2,iterations,dklen)
