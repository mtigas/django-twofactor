from django.db import models
from django_twofactor.util import random_seed, encrypt_seed, decrypt_seed

class UserAuthToken(models.Model):
    user = models.OneToOneField("auth.User")
    encrypted_seed = models.CharField(max_length=120) # enough for 16-byte salt + 40-byte seed
    
    