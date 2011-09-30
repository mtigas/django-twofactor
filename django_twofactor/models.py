from django.db import models
from django_twofactor.util import decrypt_value, check_raw_seed, get_google_url
from base64 import b32encode
from socket import gethostname

class UserAuthToken(models.Model):
    user = models.OneToOneField("auth.User")
    encrypted_seed = models.CharField(max_length=120) #fits 16b salt+40b seed
    
    created_datetime = models.DateTimeField(
        verbose_name="created", auto_now_add=True)
    updated_datetime = models.DateTimeField(
        verbose_name="last updated", auto_now=True)
    
    def check_auth_code(self, auth_code):
        """
        Checks whether `auth_code` is a valid authentication code for this
        user, at the current time.
        """
        return check_raw_seed(decrypt_value(self.encrypted_seed), auth_code)

    def google_url(self, name=None):
        """
        The Google Charts QR code version of the seed, plus an optional
        name for this (defaults to "username@hostname").
        """
        if not name:
            username = self.user.username
            hostname = gethostname()
            name = "%s@%s" % (username, hostname)

        return get_google_url(
            decrypt_value(self.encrypted_seed),
            name
        )

    def b32_secret(self):
        """
        The base32 version of the seed (for input into Google Authenticator
        and similar soft token devices.
        """
        return b32encode(decrypt_value(self.encrypted_seed))

from django_twofactor import auth_forms
