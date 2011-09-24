from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django_twofactor.models import UserAuthToken
from django_twofactor.util import decrypt_seed, check_raw_seed

class TwoFactorAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, token=None):
        # Validate username and password first
        user_or_none = super(TwoFactorAuthBackend, self).authenticate(username, password)
        
        if user_or_none and isinstance(user_or_none, User):
            # Got a valid login. Now check token.
            try:
                token = UserAuthToken.objects.get(user=user_or_none)
            except UserAuthToken.DoesNotExist:
                # User doesn't have two-factor authentication enabled.
                return user_or_none
            
            raw_seed = decrypt_seed(token.encrypted_seed)
            validate = check_raw_seed(check_raw_seed, token)
            if (validate[0] == True):
                return user_or_none
            else:
                return None
        return user_or_none
