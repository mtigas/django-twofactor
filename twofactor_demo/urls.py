from django.conf.urls.defaults import patterns, include, url

# Replace `admin.site` with `twofactor_admin_site` before doing autodiscover
# so that we can get the default auto-registered behavior BUT use our
# `AdminSite` subclass.
from django.contrib import admin
from django_twofactor.adminsite import twofactor_admin_site
admin.site = twofactor_admin_site
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twofactor_demo.views.home', name='home'),
    # url(r'^twofactor_demo/', include('twofactor_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
