# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from utils import AddDishForm
from models import Dish, Table, FoodOrder

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
    
def logout_view(request):
    logout(request)
    return HttpResponse('Wylogowano')
#zarcie
#dodanie dania do listy dan
@login_required(login_url='/so/login')
def addDish(request):
    data = {}
    data.update(csrf(request))
    if request.method == 'POST': #jak wyslano formularza
        form = AddDishForm(request.POST)
        if form.is_valid(): #jak wszystko okej
            newDish = Dish(name=request.POST['name'],
                           prize=request.POST['prize'],
                           information=request.POST['information'],
                           inscribeBy=request.user)
            newDish.save()
            return HttpResponse("Dodano danie")
    else:
        form = AddDishForm()
        data['form']=form
        data['user']=request.user;
        return render_to_response('addDish.html',data)
    
#edycja dania do listy dan
@login_required(login_url='/so/login')
def editDish(request,dish_id):
    data = {}
    data.update(csrf(request))
    editedDish = Dish.objects.get(pk=dish_id)
    if request.method == 'POST': #jak wyslano formularza
        form = AddDishForm(request.POST)
        if form.is_valid(): #jak wszystko okej
            #to pozmieniaj dane
            editedDish.name=form.cleaned_data['name']
            editedDish.prize=form.cleaned_data['prize']
            editedDish.information=form.cleaned_data['information']
            editedDish.save()
            #editedDish.information=editedDish.information[0:]
            #editedDish.save()
            return HttpResponse('Edytowano danie')
    else:
        
        fdata = {'name' : editedDish.name, 'prize' : editedDish.prize,
                     'information' : editedDish.information}
        form = AddDishForm(fdata)
        data['form']=form
        data['dish']=editedDish
        data['user']=request.user;
        return render_to_response('editDish.html',data)
#stolik
@login_required(login_url='/so/login')
def showTables(request):
    data = {}
    tableList = Table.objects.all()
    data['table_list']=tableList
    data['user']=request.user
    return render_to_response('tables.html',data)

#zarezerwowanie stolika, dodanie nowego zamowienia
@login_required(login_url='/so/login')
def addOrder(request,table_id):
    #wyciagnij stolik
    currentTable = Table.objects.get(pk=table_id);
    #wpisz rezerwacje
    currentTable.reserved = -11
    currentTable.save()
    #utworz nowe zamowienie
    newOrder = FoodOrder(table=currentTable,waiter=request.user)
    newOrder.save()
    #wyciagnij jego pk
    newOrderPk = newOrder.pk
    #wpisz do stolu jako rezerwacje
    currentTable.reserved = newOrderPk
    currentTable.setWaiter(request.user)
    currentTable.save()
    #i w tym miejscu bedzie przeniesienie do strony edytowania
    return HttpResponse('Zarezerwowano')
    