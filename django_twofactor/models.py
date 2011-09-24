from django.db import models
from django_twofactor.util import random_seed, encrypt_seed, decrypt_seed

class UserAuthToken(models.Model):
    user = models.OneToOneField("auth.User")
    encrypted_seed = models.CharField(max_length=120) # enough for 16-byte salt + 40-byte seed
    
    # TODO:
    # In a perfect world, the seed would be encrypted with the user's password
    # and the `encrypted_seed` value would update whenever the user changes his/her
    # password. This way, the seed stays entirely secure until the first factor (username+password)
    # has been validated.
    #  -> Is there any way to do this without going all hack-and-slash in here?