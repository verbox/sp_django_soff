#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from utils import AddDishForm, AddDishEntryForm, AddTableForm, OrderFilterForm, filterOrder, dishStatistics
from models import Dish, Table, FoodOrder, DishEntry
from django.utils.datetime_safe import datetime

@login_required(login_url='/so/login')
def start(request):
    #zakladamy, ze user juz sie zalogowal
    data = {}
    data['user'] = request.user
    return render_to_response('start.html',data)
        
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
                if request.GET['next'] is not None:
                    return redirect(request.GET['next'])
                else:
                    return redirect('so')
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
    data = {}
    data['information'] = 'Wylogowano!'
    data['back']='./'
    return render_to_response('info.html',data)
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
            #strona informacyjna
            data['information'] = 'Dodano danie!'
            data['back']='../'
            return render_to_response('info.html',data)
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
            data['information'] = 'Edytowano danie!'
            data['back']='../'
            return render_to_response('info.html',data)
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
    #glupawe, ale innego sposobu nie znam
    data['me']=request.user.first_name + ' ' + request.user.last_name
    return render_to_response('tables.html',data)

#dodanie stolika
@login_required(login_url='/so/login')
def addTable(request):
    data = {}
    data.update(csrf(request))
    if request.method == 'POST': #jak wyslano formularza
        form = AddTableForm(request.POST)
        if form.is_valid(): #jak wszystko okej
            #to pozmieniaj dane
            newTable = Table();
            newTable.maxClientsCount = form.cleaned_data['maxClients']
            newTable.addedBy = request.user
            newTable.save()
            #informacje
            data['information'] = 'Dodano stolik numer '+newTable.pk.__str__()
            data['back']='./'
            return render_to_response('info.html',data)
    else:
        form = AddTableForm()
        data['form'] = form
        return render_to_response('addTable.html',data)

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
    return redirect('/so/order/'+newOrderPk.__str__())

@login_required(login_url='/so/login')
def showOrder(request,order_id):
    data = {}
    data.update(csrf(request))
    #wyciagnij zamowienie
    currentOrder = FoodOrder.objects.get(pk=order_id)
    #formularz dodawania
    addEntryForm = AddDishEntryForm()
    #formularz
    if request.method == 'POST': #jak wyslano formularz
        addEntryForm = AddDishEntryForm(request.POST)
        if addEntryForm.is_valid(): #jak wszystko okej
            newDishEntry = DishEntry(dish = addEntryForm.cleaned_data['dish'],
                                     count = addEntryForm.cleaned_data['count'],
                                     foodOrder = currentOrder)
            newDishEntry.save()
            #zaszalejmy
            return HttpResponseRedirect(reverse('soff.so.views.showOrder',
                                            args=(currentOrder.pk,)))
    #wyciagnij liste wpisow, ktore sa przypisane do tego zarcia
    dishEntryList = currentOrder.dishentry_set.all()
    #dla kazdego wpisu wyciagnij laczna kase
    for de in dishEntryList:
        de.prize = de.count*de.dish.prize;
    data['order'] = currentOrder
    data['delist'] = dishEntryList
    data['sum'] = currentOrder.prize()
    data['user'] = request.user
    data['addEntryForm'] = addEntryForm
    return render_to_response('order.html',data)

#wyrzuc dana pozycje
@login_required(login_url='/so/login')
def delEntry(request,entry_id):
    #wyciagnij pozycje
    dishEntry = DishEntry.objects.get(pk=entry_id)
    #wyciagnij pk zamowienia, aby do niego wrocic
    orderPk = dishEntry.foodOrder.pk
    #kasuj
    dishEntry.delete()
    #i wroc do zamowienia
    return redirect('/so/order/'+orderPk.__str__())

#zmien status zamowienia - taki pseudo widok
@login_required(login_url='/so/login')
def changeOrderState(request,order_id,new_state):
    #wyciagnij pozycje
    order = FoodOrder.objects.get(pk=order_id)
    #nadaj orderowi nowy status
    order.state = new_state
    #i teraz tak - jak jest zapłacone, to posprzątaj stolik
    if new_state == 'ZA':
        #wpisz datę zapłacenia
        order.endDate = datetime.now()
        #wyciągnij stolik
        table = order.table
        #pozostaw stolik wolnym
        table.reserved=-1
        table.setBlankWaiter()
        table.save()
    #zapis
    order.save()
    #i wroc do zamowienia
    return HttpResponseRedirect(reverse('soff.so.views.showOrder',
            args=(order.pk,)))
    
#lista zamówień
@login_required(login_url='/so/login')
def orderList(request):
    data = {}
    data.update(csrf(request))
    #tutaj formularze do filtrowania
    if request.method == 'POST':
        formF = OrderFilterForm(request.POST)
        if formF.is_valid():
            orders = filterOrder(formF)
            ordersSum = 0
            for order in orders:
                order.sum = order.prize()
                ordersSum += order.sum
            data['formF']=formF
            data['orders']=orders
            data['user']=request.user
            data['sum']=ordersSum
            return render_to_response('orders.html',data)
    else:
        formF = OrderFilterForm()
        orders = FoodOrder.objects.all()
        ordersSum = 0
        for order in orders:
            order.sum = order.prize()
            ordersSum += order.sum
        data['formF']=formF
        data['orders']=orders
        data['user']=request.user
        data['sum']=ordersSum
        return render_to_response('orders.html',data)
    
#statystyki - właściwie to samo, co lista zamówień, ale z dodatkową statystyką dań.
@login_required(login_url='/so/login')
def statistics(request):
    data = {}
    data.update(csrf(request))
    #tutaj formularze do filtrowania
    if request.method == 'POST':
        formF = OrderFilterForm(request.POST)
        if formF.is_valid():
            orders = filterOrder(formF)
            ordersSum = 0
            for order in orders:
                order.sum = order.prize()
                ordersSum += order.sum
            data['formF']=formF
            data['orders']=orders
            data['user']=request.user
            data['sum']=ordersSum
            data['statistics']=dishStatistics(orders)
            return render_to_response('statistics.html',data)
    else:
        formF = OrderFilterForm()
        orders = FoodOrder.objects.all()
        ordersSum = 0
        for order in orders:
            order.sum = order.prize()
            ordersSum += order.sum
        data['formF']=formF
        data['orders']=orders
        data['user']=request.user
        data['sum']=ordersSum
        data['statistics']=dishStatistics(orders)
        return render_to_response('statistics.html',data)