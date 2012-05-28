#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

#Klasa reprezentująca pojedynczy stolik
class Table(models.Model):
    maxClientsCount = models.IntegerField(default=4)
    reserved = models.ForeignKey(User)
    def __unicode__(self):
        return self.pk + " " +self.maxClientsCount

#User = pracownik

#Zamowienie, skladajace sie z listy wpisow, kelnera (pracownika-Usera),
#stolika i ewentualnego komentarza do zamowienia
#Z pol "obslugowych"
class FoodOrder(models.Model):
    #lista wpisow w zamowieniu - z automatu
    waiter = models.ForeignKey(User)
    table = models.ForeignKey(Table)
    comment = models.TextField()

#Reprezentuje żarcie - tj. dane dotyczące pojedynczego dania, napoju itp.   
class Dish(models.Model):
    name = models.CharField(max_length=100)
    addedDate = models.DateField(auto_now_add=True)
    prize = models.DecimalField(max_digits=50,decimal_places=2)
    #waga - w gramach
    information = models.TextField()
    #kto wprowadzil
    inscribeBy = models.ForeignKey(User)
    
#Wpis w zamowieniu - para Danie-il.sztuk
class DishEntry(models.Model):
    dish = models.ForeignKey(Dish)
    foodOrder = models.ForeignKey(FoodOrder)
    count = models.IntegerField(default=1)