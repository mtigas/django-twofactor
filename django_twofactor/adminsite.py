from django.contrib.admin.sites import AdminSite
from django_twofactor.auth_forms import TwoFactorAdminAuthenticationForm

class TwoFactorAuthAdminSite(AdminSite):
    login_form = TwoFactorAdminAuthenticationForm
    login_template = "admin/twofactor_login.html"

twofactor_admin_site = TwoFactorAuthAdminSite()
