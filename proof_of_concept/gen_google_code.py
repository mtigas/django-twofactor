from base64 import b32encode
from binascii import hexlify, unhexlify
import random
import socket
import sys
from urllib import urlencode

# Secure random generators
try:
    random = random.SystemRandom()
except:
    pass
try:
    from os import urandom
except:
    urandom = None

##########

def random_seed(rawsize=10):
    """ Generates a random seed, which is hex encoded. """
    if urandom:
        randstr = urandom(rawsize)
    else:
        randstr = ''.join([ chr(random.randint(0, 255)) for i in range(rawsize) ])
    return hexlify(randstr)

def get_google_url(hex_secret, hostname=None):
    # Note: Google uses base32 for it's encoding rather than hex.
    b32secret = b32encode( unhexlify(hex_secret) )
    if not hostname:
        hostname = socket.gethostname()
    
    data = "otpauth://totp/%(hostname)s?secret=%(secret)s" % {
        "hostname":hostname,
        "secret":b32secret,
    }
    url = "https://chart.googleapis.com/chart?" + urlencode({
        "chs":"200x200",
        "chld":"M|0",
        "cht":"qr",
        "chl":data
    })
    return b32secret, url

##########

if __name__ == "__main__":
    secret = random_seed()
    
    b32secret, url = get_google_url(secret, )

    print "Hex secret: %s" % secret
    print "...base32:  %s" % b32secret
    print
    print "===== Google URL ====="
    print "Scan this with Google Authenticator or enter the base32"
    print "value above as 'key' when manually adding.\n    %s" % url
    print
    print "(See http://www.google.com/support/accounts/bin/answer.py?answer=1066447 )"
    