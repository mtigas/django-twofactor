from binascii import hexlify
from django_twofactor.encutil import encrypt, decrypt, _gen_salt
from oath import accept_totp

# Secure random generators
import random
try:
    random = random.SystemRandom()
except:
    pass
try:
    from os import urandom
except:
    urandom = None

def random_seed(rawsize=10):
    """ Generates a random seed as a raw byte string. """
    if urandom:
        randstr = urandom(rawsize)
    else:
        randstr = ''.join([ chr(random.randint(0, 255)) for i in range(rawsize) ])
    return randstr

def encrypt_seed(raw_seed):
    salt = _gen_salt()
    return "%s$%s" %  (salt, encrypt(raw_seed, salt))

def decrypt_seed(salted_seed):
    salt, encrypted_seed = salted_seed.split("$", 1)
    return decrypt(encrypted_seed, salt)

def check_raw_seed(raw_seed, auth_code, token_type="dec6"):
    return accept_totp(auth_code, hexlify(raw_seed), token_type)