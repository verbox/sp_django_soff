# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def start(request):
    data = {}
    data.update(csrf(request))
    if request.method == 'POST': # Juz po wyslaniu formularza
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse("Zalogowany!")
            else:
                return HttpResponse("Zablokowany!!!")
        else:
            return HttpResponse("Bledny user/haslo")
    else:
        if request.user.is_authenticated():
            #strona startowa
            return HttpResponse("User: "+request.user.username+", w tym miejscu bedzie strona startowa")
        else:
            form = AuthenticationForm()
            data['form']=form
            return render_to_response('start.html',data)