from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from django.conf import settings
from django.shortcuts import render

class LoginView(TemplateView):
    template_name = 'auth/login.html'
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return render(request, "index.html")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)