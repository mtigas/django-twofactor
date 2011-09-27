from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django_twofactor.adminsite import twofactor_admin_site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twofactor_demo.views.home', name='home'),
    # url(r'^twofactor_demo/', include('twofactor_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(twofactor_admin_site.urls)),
)
