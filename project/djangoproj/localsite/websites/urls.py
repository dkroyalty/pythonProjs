from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # the prev hit pattern is removed, all followed url begins with '/websites/'
    url(r'^$', views.websites, name='websites'),
    url(r'^edit/(?P<operation>.*)/(?P<param>.*)/$', views.webedit, name='webedit'),
]
