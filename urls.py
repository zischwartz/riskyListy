from django.conf.urls.defaults import patterns, include, url

from django.views.generic import ListView, DetailView
from django.views.generic.simple import direct_to_template

from interface.models import Team, Player, Emailer

from django.contrib import admin
admin.autodiscover()

teamDetail = DetailView.as_view(model=Team, template_name= "teamDetail.html")


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'interface.views.home', name='home'),
    url(r'^team/(?P<pk>[a-z\d]+)/$', teamDetail, name='teamDetail'),

    (r'^accounts/', include('registration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
