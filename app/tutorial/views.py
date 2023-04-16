from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from django.conf import settings
from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')