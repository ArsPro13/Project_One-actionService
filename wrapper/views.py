from django.shortcuts import render
from django.http import HttpResponse

from . import services

views = []

def wrap(f):
    def my_view(request):
       return HttpResponse(str(f()))
    my_view.__name__ =  f.__name__
    return my_view

for n in dir(services):
    if "_" not in n:
        views.append(wrap(getattr(services, n)))

