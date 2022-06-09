#https://1drv.ms/b/s!ArA-DhLm6QVXiK5UE-eEcEZxLB0-2w
import hashlib

def hash(hasher, password, salt):
  to_be_hashed = (salt + password).encode()
  hasher.update(to_be_hashed)
  return salt + hasher.hexdigest()  

def cria_hasher(cryptography):
    if cryptography.upper() == 'SHA256':
        return hashlib.sha256()
    elif cryptography.upper() == 'SHA512':
        return hashlib.sha512()
    elif cryptography.upper() == 'SHA1':
        return hashlib.sha1()
    elif cryptography.upper() == 'MD5':
        return hashlib.md5()
    elif cryptography.upper() == 'SHA384':
        return hashlib.sha384()
    elif cryptography.upper() == 'SHA224':
        return hashlib.sha224()
    elif cryptography.upper() == 'BLAKE2B':
        return hashlib.blake2b()
    elif cryptography.upper() == 'BLAKE2S':
        return hashlib.blake2s()
    else:
        return - 1
#teste

def generate_hashed_password(cryptography, password, salt, iterations, dklen):
    derivatekey = ''
    hasher = cria_hasher(cryptography)
    if hasher == -1:
      return -1
    for c in range (dklen):
        for k in range (iterations):
            password = hash(hasher, password, salt)
        derivatekey += password[32]
    return derivatekey
