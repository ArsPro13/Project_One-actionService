from __future__ import annotations
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from urllib import request

from . import services
from .forms import OurForm

views = []

def args(f):
    return(f.__annotations__)

def wrap(request):
    if (request.method == 'POST'):
        form = OurForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = OurForm()

    return render(request, 'name.html', {'form': form})



#for n in dir(services):
#    if "_" not in n:
#        views.append(wrap(getattr(services, n)))

