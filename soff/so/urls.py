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
    url(r'^dish$',ProtectedListView.as_view(queryset=Dish.objects.all(),
                                           template_name="dishes.html" )),
    #lista stolikow (albo stolik=link, gdy dany kelner juz "obsluguje" dany 
    #stolik - wtedy przenosi na dane zamowienie, albo pusty + przycisk rezerwuj)
    #dane zamowienie
    #utworz zamowienie
    #dodaj wpis do zamowienia
    #zmien stan zamowienia
    url(r'^', 'start'),
)
