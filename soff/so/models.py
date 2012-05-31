#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

#Klasa reprezentująca pojedynczy stolik
class Table(models.Model):
    maxClientsCount = models.IntegerField(default=4)
    reserved = models.IntegerField(default=-1)
    #nie wiem, jak wywolac funkcje w szablonie - dlatego tak obejdziemy problem
    currentWaiter = models.CharField(default='---',max_length=100)
    def __unicode__(self):
        return self.pk.__str__() + ' ' +self.maxClientsCount.__str__()
    def setWaiter(self,waiter):
        self.currentWaiter = waiter.first_name + ' ' + waiter.last_name
    def setBlankWaiter(self):
        self.currentWaiter = '---'
#User = pracownik

#Zamowienie, skladajace sie z listy wpisow, kelnera (pracownika-Usera),
#stolika i ewentualnego komentarza do zamowienia
#Z pol "obslugowych"
class FoodOrder(models.Model):
    ORDER_STATE = (
                   ('NO','Nowe'),
                   ('WR','W trakcie realizacji'),
                   ('ZR','Zrealizowane'),
                   ('ZA','Zapłacone'),
                   )
    
    #lista wpisow w zamowieniu - z automatu
    waiter = models.ForeignKey(User)
    table = models.ForeignKey(Table)
    comment = models.TextField()
    state = models.CharField(max_length=50, choices=ORDER_STATE, default='NO')
    def prize(self):
        wynik = 0.0
        #wyciagnij liste DishEntry i pojedz po niej
        for entry in self.dishentry_set.all():
            wynik=wynik+entry.count*entry.dish.prize
        return wynik

#Reprezentuje żarcie - tj. dane dotyczące pojedynczego dania, napoju itp.   
class Dish(models.Model):
    name = models.CharField(max_length=100)
    addedDate = models.DateField(auto_now_add=True)
    prize = models.FloatField()
    #waga - w gramach
    information = models.TextField()
    #kto wprowadzil
    inscribeBy = models.ForeignKey(User)
    
    def __unicode__(self):
        return '('+self.pk.__str__()+') '+self.name
#Wpis w zamowieniu - para Danie-il.sztuk
class DishEntry(models.Model):
    dish = models.ForeignKey(Dish)
    foodOrder = models.ForeignKey(FoodOrder)
    count = models.IntegerField(default=1)