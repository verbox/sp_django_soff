from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('soff.so.views',
   
    url(r'^login$','login'),                   
    url(r'^', 'start'),

)
