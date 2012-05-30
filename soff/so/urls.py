from django.conf.urls.defaults import patterns, include, url
from utils import ProtectedListView
from models import *
urlpatterns = patterns('soff.so.views',

    url(r'^login$','login'),
    url(r'^logout_view$','logout_view'),
    #zwiazane z zarciami
    #dodaj zarcie
    url(r'^dish/add','addDish'),
    #edytuj danie
    url(r'^dish/edit/(?P<dish_id>\d+)','editDish'),
        #lista zarc                   
    url(r'^dish',ProtectedListView.as_view(queryset=Dish.objects.all(),
                                           template_name="dishes.html" )),
    #lista stolikow (albo stolik=link, gdy dany kelner juz "obsluguje" dany 
    #stolik - wtedy przenosi na dane zamowienie, albo pusty + przycisk rezerwuj 
    #i przenosi na tworzenie nowego zamowienia
    url(r'^table','showTables'),
    #dane zamowienie (szczegoly)
    #url(r'^order/(?P<order_id>\d+)','showOrder'),
    #utworz zamowienie
    url(r'^order/add/(?P<table_id>\d+)','addOrder'), #f
    #dodaj wpis do zamowienia
    #url(r'^order/addEntry/(?P<order_id>\d+)','addOrderEntry'), #f
    #zmien stan zamowienia
    #url(r'^order/changeState/(?P<order_id>\d+)/(?P<new_state>\w+','changeOrderState'),
    url(r'^', 'start'),
)
