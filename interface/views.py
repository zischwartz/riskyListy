
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime


from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response
from django.utils import simplejson

import settings
from models import *


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/edit')
    return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def getTeam(request, id):
    team = get_object_or_404(Team, id=id)
    # team_players = get_list_or_404(MyModel, )
    return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def editTeam(request):
    if request.user.is_authenticated():
        team = get_object_or_404(Team, user=request.user)
        team_players = get_list_or_404(Player, team=team )
        return render_to_response("editTeam.html", locals() , context_instance=RequestContext(request))
    else:
        return HttpResponse('error yo')

def addPlayer(request, id):
    if request.user.is_authenticated():
        team = get_object_or_404(Team, user=request.user)
        emailer_to_add = get_object_or_404(Emailer, id=id)
        new_player = Player.objects.create(team=team, emailer=emailer_to_add, points= 0) # Points should be 0 when they're first added no matter what, right?
        return HttpResponseRedirect('/edit')
    else:
        return HttpResponse('error yo')


def removePlayer(request, id):
    if request.user.is_authenticated():
        team = get_object_or_404(Team, user=request.user)
        team_players = get_list_or_404(Player, team=team )
        player_to_remove = get_object_or_404(Player, id=id)
        if player_to_remove in team_players:
            player_to_remove.delete()
            return HttpResponseRedirect('/edit')
        else:
            return HttpResponse('You cheater! Trying to edit someone elses team? ')
    else:
        return HttpResponse('error yo')

