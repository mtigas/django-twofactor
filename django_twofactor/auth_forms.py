from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _



AuthenticationForm.token = forms.IntegerField(label=_("Authentication Token"),
    max_length=6
    min_value=100000, max_value=999999,
    required=False
)

def _clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    token = self.cleaned_data.get('token')

    if username and password:
        self.user_cache = authenticate(username=username, password=password, token=token)
        if self.user_cache is None:
            raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
        elif not self.user_cache.is_active:
            raise forms.ValidationError(_("This account is inactive."))
    self.check_for_test_cookie()
    return self.cleaned_data

AuthenticationForm.clean = clean
