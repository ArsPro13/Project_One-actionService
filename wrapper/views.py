from __future__ import annotations
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from urllib import request
from django import forms
from django.db import models
from copy import copy
from . import services
from .types import Text, File 
from .forms import GeeksForm

views = []

def args(f):
    return(f.__annotations__)

def field(s, i):
    print(type(s))
    if (s == int):
        return forms.IntegerField(label = i)
    if (s == str):
        return forms.CharField(label = i)
    if (s == Text):
        return forms.CharField(label = i, widget=forms.Textarea)


def wrap(f):
    def my_view(request):
        arguments = copy(args(f))
        temp = {}
        for i in arguments:
            if (arguments[i] == File):
                temp[i] = forms.FileField()
            else:
                temp[i] = field(arguments[i], i)

        if (request.method == 'POST'):
            form = type('MyF', (forms.Form, ), temp)()
            for i in arguments.keys():
                types = copy(f.__annotations__)
                if (types[i] != File):
                    arguments[i] = types[i](request.POST[i])
                else:
                    arguments[i] = request.FILES['a'].read()
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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = 'Invalid login credentials'
    else:
        message = ''
    return render(request, 'login.html', {'message': message})


def home(request):
    return render(request, 'home.html')