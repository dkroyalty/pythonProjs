"""localsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from localsite import settings
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^error/$', views.error, name='error'),
    url(r'^index/$', views.index, name='index'),
    # url(r'^favicon\.ico/$', 'django.views.generic.simple.redirect_to',
    #     {'url': '/static/img/favicon.ico'}),
    url(r'/static/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.STATICFILES_DIRS[0]}),
    url(r'^favicon\.ico/$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^websites/', include('localsite.websites.urls')),
    url(r'^saas/', include('localsite.saas.urls')),
]

urlpatterns += staticfiles_urlpatterns()
