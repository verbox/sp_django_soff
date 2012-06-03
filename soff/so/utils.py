#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django import forms
from models import Dish

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
    
class ChangeOrderStatusForm(forms.Form):
    ORDER_STATE = (
                   ('NO','Nowe'),
                   ('WR','W trakcie realizacji'),
                   ('ZR','Zrealizowane'),
                   ('ZA','Zapłacone'),
                   )
    state = forms.ChoiceField(label='Status:',choices=ORDER_STATE)
    #nie wiem, jak dostac sie do inital z pola state, wiec jade naokolo
    def setState(self,newState):
        self.state = newState
        
