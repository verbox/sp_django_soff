from django.conf.urls.defaults import patterns, include, url
from utils import ProtectedListView
from models import *
urlpatterns = patterns('soff.so.views',

    url(r'^login$','login'),                   
    url(r'^dish',ProtectedListView.as_view(queryset=Dish.objects.all(),
                                           template_name="dishes.html" )),
    url(r'^', 'start'),
)
