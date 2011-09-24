"""
Kind of based on the encryption bits detailed in
http://djangosnippets.org/snippets/1095/
"""

from hashlib import sha256
#from django.conf import settings
from django.utils.encoding import smart_str
from binascii import hexlify, unhexlify
import string
try:
    from Crypto.Cipher import AES
except ImportError:
    from django_twofactor import pyaes as AES

import random
try:
    random = random.SystemRandom()
except:
    pass

def _gen_salt(length=16):
    return ''.join([random.choice(string.letters+string.digits) for i in range(length)])

def _get_key(salt):
    """ Combines `settings.SECRET_KEY` with a salt. """
    if not salt: salt = ""
    
    return sha256("%s%s" % ("ASDF", salt)).digest()

def encrypt(data, salt):
    cipher = AES.new(_get_key(salt), mode=AES.MODE_ECB)
    value = smart_str(data)

    padding  = cipher.block_size - len(value) % cipher.block_size
    if padding and padding < cipher.block_size:
        value += "\0" + ''.join([random.choice(string.printable) for index in range(padding-1)])
    return hexlify(cipher.encrypt(value))

def decrypt(encrypted_data, salt):
    cipher = AES.new(_get_key(salt), mode=AES.MODE_ECB)

    return cipher.decrypt(unhexlify(smart_str(encrypted_data))).split('\0')[0]
