from binascii import hexlify
from django_twofactor.encutil import encrypt, decrypt, _gen_salt
from oath import accept_totp

# Get best `random` implementation we can.
import random
try:
    random = random.SystemRandom()
except:
    pass

def random_seed(rawsize=10):
    """ Generates a random seed as a raw byte string. """
    return ''.join([ chr(random.randint(0, 255)) for i in range(rawsize) ])

def encrypt_value(raw_value):
    salt = _gen_salt()
    return "%s$%s" %  (salt, encrypt(raw_value, salt))

def decrypt_value(salted_value):
    salt, encrypted_value = salted_value.split("$", 1)
    return decrypt(encrypted_value, salt)

def check_raw_seed(raw_seed, auth_code, token_type="dec6"):
    """
    Checks whether `auth_code` is a valid authentication code at the current time,
    based on the `raw_seed` (raw byte string representation of `seed`).
    """
    return accept_totp(auth_code, hexlify(raw_seed), token_type)[0]
    