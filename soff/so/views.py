# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from utils import AddDishForm
from models import Dish

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
                return redirect(request.GET['next'])
            else:
                return HttpResponse("Zablokowany!!!")
        else:
            return HttpResponse("Bledny user/haslo")
    else:
        form = AuthenticationForm()
        data['form']=form
        return render_to_response('login.html',data)
    
@login_required(login_url='/so/login')
def addDish(request):
    data = {}
    data.update(csrf(request))
    if request.method == 'POST': #jak wyslano formularza
        form = AddDishForm(request.POST)
        if form.is_valid(): #jak wszystko okej
            newDish = Dish(name=request.POST['nazwa'],
                           prize=request.POST['cena'],
                           information=request.POST['informacje'],
                           inscribeBy=request.user)
            newDish.save()
            return HttpResponse("Dodano danie")
    else:
        form = AddDishForm()
        data['form']=form
        data['user']=request.user;
        return render_to_response('addDish.html',data)
    