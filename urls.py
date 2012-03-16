from django.conf.urls.defaults import patterns, include, url

# import registration.backends.default.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'interface.views.home', name='home'),
    (r'^accounts/', include('registration.urls')),
    # url(r'^riskyListy/', include('riskyListy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
