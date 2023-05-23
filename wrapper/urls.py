from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from . import views

def reg(request):
    return HttpResponseRedirect("/login")

urlpatterns = [
    path('', reg),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
]