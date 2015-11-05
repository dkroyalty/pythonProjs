from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # the prev hit pattern is removed, all followed url begins with '/websites/'
    url(r'^tax$', views.taxCalc, name='taxcalc'),
    url(r'^place/disp$', views.placeDisp, name='placedisp'),
    url(r'^place/edit$', views.placeEdit, name='placeedit'),
    url(r'^place/edit/confirm$', views.placeEditConfirm, name='placeeditconfirm'),
    url(r'^item/edit$', views.itemEdit, name='itemedit'),
    url(r'^item/edit/confirm$', views.itemEditConfirm, name='itemeditconfirm'),
    url(r'^item/edittype$', views.itemEditType, name='itemedittype'),
    url(r'^item/editstatus$', views.itemEditStatus, name='itemeditstatus'),
]
