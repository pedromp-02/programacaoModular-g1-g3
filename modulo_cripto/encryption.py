import hashlib

def hash(hasher, password, salt):
  to_be_hashed = (salt + password).encode()
  hasher.update(to_be_hashed)
  return salt + hasher.hexdigest()  


def generate_hashed_password(cryptography, password, salt, iterations, dklen):
    derivatekey = ''
    if cryptography.upper() == 'SHA256':
        hasher = hashlib.sha256()
    elif cryptography.upper() == 'SHA512':
        hasher = hashlib.sha512()
    elif cryptography.upper() == 'SHA1':
        hasher = hashlib.sha1()
    elif cryptography.upper() == 'MD5':
        hasher = hashlib.md5()
    elif cryptography.upper() == 'SHA384':
        hasher = hashlib.sha384()
    elif cryptography.upper() == 'SHA224':
        hasher = hashlib.sha224()
    elif cryptography.upper() == 'BLAKE2B':
        hasher = hashlib.blake2b()
    elif cryptography.upper() == 'BLAKE2S':
        hasher = hashlib.blake2s()
    else:
        return - 1
    for c in range (dklen):
        for k in range (iterations):
            password = hash(hasher, password, salt)
        derivatekey += password[32]
    return derivatekey
