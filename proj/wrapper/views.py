from __future__ import annotations
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from urllib import request
from django import forms

from . import services

views = []

def args(f):
    return(f.__annotations__)

def wrap(f):
    def my_view(request):
        arguments = args(f)
        temp = {}
        for i in arguments:
            temp[i] = forms.CharField(label = i)
        
        if (request.method == 'POST'):
            form = type('MyF', (forms.Form, ), temp)()
            for  i in arguments.keys():
                arguments[i] = request.POST[i]
            
            res = f(**arguments)
            
            #в f передаем словарь
        else:
            form = type('MyF', (forms.Form, ), temp)()
            res = None
        return render(request, 'trial.html', {'form':  form, 'res': str(res)})
    my_view.__name__ =  f.__name__
    return my_view


for n in dir(services):
    if "_" not in n:
        views.append(wrap(getattr(services, n)))

