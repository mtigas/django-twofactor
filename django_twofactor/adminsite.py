from django.contrib.admin.sites import AdminSite
from django_twofactor.auth_forms import TwoFactorAdminAuthenticationForm
from django_twofactor.forms import ResetTwoFactorAuthForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_twofactor.models import UserAuthToken

class TwoFactorAuthAdminSite(AdminSite):
    login_form = TwoFactorAdminAuthenticationForm
    login_template = "twofactor_admin/twofactor_login.html"
    password_change_template = "twofactor_admin/registration/password_change_form.html"

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('django_twofactor.admin_views',
            url(r'^twofactor_auth_setup/$',
                self.twofactor_config,
                name="twofactor_config"),
        )
        urlpatterns += super(TwoFactorAuthAdminSite, self).get_urls()

        return urlpatterns
    
    def twofactor_config(self, request):
        """
        Handles two-factor authenticator configuration.
        """
        f = None
        if request.method == "POST":
            f = ResetTwoFactorAuthForm(user=request.user, data=request.POST)
            if f.is_valid():
                token = f.save()
                return render_to_response(
                    "twofactor_admin/registration/twofactor_config_done.html",
                    dict(form=f, token=token, user=request.user),
                    context_instance=RequestContext(request)
                )
        if not f:
            f = ResetTwoFactorAuthForm(user=None)
        has_token = bool(UserAuthToken.objects.filter(user=request.user))

        return render_to_response(
            "twofactor_admin/registration/twofactor_config.html",
            dict(form=f, has_token=has_token),
            context_instance=RequestContext(request)
        )


twofactor_admin_site = TwoFactorAuthAdminSite()
