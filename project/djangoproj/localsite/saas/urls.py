from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # the prev hit pattern is removed, all followed url begins with '/websites/'
    url(r'^tax$', views.taxcalc, name='taxcalc'),
    url(r'^place$', views.placetop, name='place'),
]
