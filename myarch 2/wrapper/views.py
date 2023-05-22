from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from . import services

views = []

def wrap(f):
    def my_view(request):
       user_id = request.user.id
       return HttpResponse(str(f()))
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
            return redirect('/admin')
        else:
            message = 'Invalid login credentials'
    else:
        message = ''
    return render(request, 'login.html', {'message': message})