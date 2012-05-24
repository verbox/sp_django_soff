from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django import forms

#klasa na potrzeby zabezpieczenia widokow generycznych
class ProtectedListView(ListView):
    @method_decorator(login_required(login_url='/so/login'))
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)

class AddDishForm(forms.Form):
    nazwa = forms.CharField()
    cena = forms.DecimalField()
    informacje = forms.CharField(widget=forms.Textarea)
