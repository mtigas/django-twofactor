from django.contrib.admin.sites import AdminSite
from django_twofactor.auth_forms import TwoFactorAdminAuthenticationForm
from django_twofactor.forms import (ResetTwoFactorAuthForm,
    DisableTwoFactorAuthForm)
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
        disableform = None
        resetform = None
        if (request.method == "POST")\
        and ("reset_confirmation" in request.POST):
            # We are resetting the user's two-factor key.
            resetform = ResetTwoFactorAuthForm(user=request.user,
                data=request.POST)
            if resetform.is_valid():
                token = resetform.save()
                return render_to_response(
                    "twofactor_admin/registration/twofactor_config_done.html",
                    dict(token=token, user=request.user),
                    context_instance=RequestContext(request)
                )
        elif (request.method == "POST")\
        and ("disable_confirmation" in request.POST):
            # We are disabling two-factor auth for the user
            disableform = DisableTwoFactorAuthForm(user=request.user,
                data=request.POST)
            if disableform.is_valid():
                disableform.save()
                return render_to_response(
                    "twofactor_admin/registration/twofactor_config_disabled.html",
                    dict(user=request.user),
                    context_instance=RequestContext(request)
                )
        if not resetform:
            resetform = ResetTwoFactorAuthForm(user=None)
        if not disableform:
            disableform = DisableTwoFactorAuthForm(user=None)

        has_token = bool(UserAuthToken.objects.filter(user=request.user))

        return render_to_response(
            "twofactor_admin/registration/twofactor_config.html",
            dict(
                resetform=resetform,
                disableform=disableform,
                has_token=has_token
            ),
            context_instance=RequestContext(request)
        )


twofactor_admin_site = TwoFactorAuthAdminSite()
