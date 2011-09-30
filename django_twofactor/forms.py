from django import forms
from django_twofactor.models import UserAuthToken
from django_twofactor.util import random_seed, encrypt_value

class ResetTwoFactorAuthForm(forms.Form):
    confirmation = forms.BooleanField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ResetTwoFactorAuthForm, self).__init__(*args, **kwargs)

    def save(self):
        if not self.user:
            return None

        try:
            token = UserAuthToken.objects.get(user=self.user)
        except UserAuthToken.DoesNotExist:
            token = UserAuthToken(user=self.user)

        token.encrypted_seed = encrypt_value(random_seed(30))
        token.save()
        return token

