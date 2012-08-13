from base64 import b32encode
from binascii import hexlify
from urllib import urlencode
from django_twofactor.encutil import encrypt, decrypt, _gen_salt
from oath import accept_totp
from django.conf import settings

# Get best `random` implementation we can.
import random
try:
    random = random.SystemRandom()
except:
    pass

# Parse out some settings, if we have 'em.
TOTP_OPTIONS = getattr(settings, "TWOFACTOR_TOTP_OPTIONS", {})
PERIOD = TOTP_OPTIONS.get('period', 30)
FORWARD_DRIFT = TOTP_OPTIONS.get('forward_drift', 1)
BACKWARD_DRIFT = TOTP_OPTIONS.get('backward_drift', 1)

# note: Google Authenticator only outputs dec6, so changing this
# will result in incompatibility
DEFAULT_TOKEN_TYPE = TOTP_OPTIONS.get('default_token_type', "dec6")

ENCRYPTION_KEY = getattr(settings, "TWOFACTOR_ENCRYPTION_KEY", "")

def random_seed(rawsize=10):
    """ Generates a random seed as a raw byte string. """
    return ''.join([ chr(random.randint(0, 255)) for i in range(rawsize) ])

def encrypt_value(raw_value):
    salt = _gen_salt()
    return "%s$%s" %  (salt, encrypt(raw_value, ENCRYPTION_KEY+salt))

def decrypt_value(salted_value):
    salt, encrypted_value = salted_value.split("$", 1)
    return decrypt(encrypted_value, ENCRYPTION_KEY+salt)

def check_raw_seed(raw_seed, auth_code, token_type=None):
    """
    Checks whether `auth_code` is a valid authentication code at the current time,
    based on the `raw_seed` (raw byte string representation of `seed`).
    """
    if not token_type:
        token_type = DEFAULT_TOKEN_TYPE
    return accept_totp(
        auth_code,
        hexlify(raw_seed),
        token_type,
        period=PERIOD,
        forward_drift=FORWARD_DRIFT,
        backward_drift=BACKWARD_DRIFT
    )[0]

def get_google_url(raw_seed, hostname=None):
    # Note: Google uses base32 for it's encoding rather than hex.
    b32secret = b32encode( raw_seed )
    if not hostname:
        from socket import gethostname
        hostname = gethostname()
    
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
    return url
