from django.conf.urls.defaults import patterns, include, url
from django_twofactor.auth_forms import TwoFactorAuthenticationForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Replace `admin.site` with `twofactor_admin_site` before doing autodiscover
# so that we can get the default auto-registered behavior BUT use our
# `AdminSite` subclass.
from django.contrib import admin
from django_twofactor.adminsite import twofactor_admin_site
admin.site = twofactor_admin_site
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'django.contrib.auth.views.login', {
        'template_name': 'login.html',
        'authentication_form': TwoFactorAuthenticationForm
    }),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {
        'login_url': '/'
    }),
) + staticfiles_urlpatterns()
