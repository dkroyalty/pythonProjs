# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

import datetime
from websites.views import *

def getNowTime():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def index(request):
    htmltemplate = get_template('index.html')
    paramdict = {
        'time' : getNowTime(),
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)

def websites(request):
    htmltemplate = get_template('websites.html')
    paramdict = {
        'weblist' : getOrderedWebList(),
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)
