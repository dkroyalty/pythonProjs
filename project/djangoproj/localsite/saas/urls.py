from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # the prev hit pattern is removed, all followed url begins with '/websites/'
    url(r'^tax$', views.taxCalc, name='taxcalc'),
    url(r'^place/disp$', views.placeDisp, name='placedisp'),
    url(r'^place/edit$', views.placeEdit, name='placeedit'),
]
