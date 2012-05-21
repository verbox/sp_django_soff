# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url='/so/login')
def start(request):
    #zakladamy, ze user juz sie zalogowal
    return HttpResponse("User: "+request.user.username+", w tym miejscu bedzie strona startowa")
        
def login(request):
    data = {}
    data.update(csrf(request))
    if request.method == 'POST': # Juz po wyslaniu formularza
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return HttpResponse("Zalogowany!")
            else:
                return HttpResponse("Zablokowany!!!")
        else:
            return HttpResponse("Bledny user/haslo")
    else:
        form = AuthenticationForm()
        data['form']=form
        return render_to_response('login.html',data)