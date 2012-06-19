#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django import forms
from models import Dish, FoodOrder
from django.http import HttpResponse

#klasa na potrzeby zabezpieczenia widokow generycznych
class ProtectedListView(ListView):
    @method_decorator(login_required(login_url='/so/login'))
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)

class AddDishForm(forms.Form):
    name = forms.CharField(label='Nazwa')
    prize = forms.DecimalField(label='Cena')
    information = forms.CharField(label='Informacja', widget=forms.Textarea)
    
class AddDishEntryForm(forms.Form):
    dish = forms.ModelChoiceField(label='Danie',queryset = Dish.objects.all())
    count = forms.IntegerField(label='Liczba')
        
class AddTableForm(forms.Form):
    maxClients = forms.IntegerField(label='Maksymalna liczba klientów',initial=4)
    
class OrderFilterForm(forms.Form):
    #masakra
    waiters = []
    waiters.append(('W','Wszyscy'))
    #wrzuc wszystkich
    for waiter in User.objects.all():
        waiters.append((waiter.username,waiter.first_name+' '+waiter.last_name))
    selectWaiter = forms.ChoiceField(label='Pracownik',choices=waiters)
    
def filterOrder(formF):
    #poprzedni krok/etap filtrowania - na poczatku lista wszystkich
    prevStep = FoodOrder.objects.all()
    #nastepny krok - zamowienia po filtrowaniu
    nextStep = []
    #---FILTROWANIE PO KELNERZE---
    selectedWaiter = formF.data['selectWaiter']
    if selectedWaiter == 'W':
        nextStep.extend(prevStep)
    else:
        #idz po wszystkich zamowieniach i wylow te z danym kelnerem
        for order in prevStep:
            if order.waiter.username == selectedWaiter:
                nextStep.append(order)
    #---KONIEC FILTROWANIA PO KELNERZE---
    return nextStep
    
    