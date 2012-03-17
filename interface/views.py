
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
    return render_to_response("home.html", locals() , context_instance=RequestContext(request))

def getTeam(request, id):
    team = get_object_or_404(Team, id=id)
    # team_players = get_list_or_404(MyModel, )
    return render_to_response("home.html", locals() , context_instance=RequestContext(request))

