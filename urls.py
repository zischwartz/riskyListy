from django.conf.urls.defaults import patterns, include, url

from django.views.generic import ListView, DetailView
from django.views.generic.simple import direct_to_template

from interface.models import Team, Player, Emailer

from django.contrib import admin
admin.autodiscover()

teamDetail = DetailView.as_view(model=Team, template_name= "teamDetail.html")
emailerDetail = DetailView.as_view(model=Emailer, template_name= "emailerDetail.html")

emailerList = ListView.as_view(model=Emailer, template_name= "emailerList.html")
# teamList = ListView.as_view(model=Team, template_name= "teamList.html")


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'interface.views.home', name='home'),
    url(r'^team/(?P<pk>[a-z\d]+)/$', teamDetail, name='teamDetail'),
    url(r'^emailers/$', emailerList, name='emailerList'),
    url(r'^teams/$', 'interface.views.teamList', name='teamList'),
    url(r'^emailer/(?P<pk>[a-z\d]+)/$', emailerDetail, name='emailerDetail'),

    url(r'^help/$', direct_to_template, {'template': 'help.html'}),

    url(r'^edit/?$', 'interface.views.editTeam', name='editTeam'),
    url(r'^remove/?(?P<id>[a-z\d]+)/$', 'interface.views.removePlayer'),
    url(r'^add/?(?P<id>[a-z\d]+)/$', 'interface.views.addPlayer'),

    (r'^accounts/profile/.*', 'interface.views.home'),
    (r'^users/.*', 'interface.views.home'),
    (r'^accounts/', include('registration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
