# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

from websites.views import *

def index(request):
    htmltemplate = get_template('index.html')
    paramdict = {
        #'time' : getNowTime(),
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)

def error(request):
    htmltemplate = get_template('error.html')
    paramdict = {
        'redirect' : '/',
        'staytime' : 10,
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)