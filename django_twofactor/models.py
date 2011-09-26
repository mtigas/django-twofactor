from django.db import models
from django_twofactor.util import decrypt_value, check_raw_seed

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
