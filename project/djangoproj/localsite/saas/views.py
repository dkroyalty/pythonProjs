# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

import datetime
from saas.views import *
from localsite.decorators import (
    valid_params,
)

def taxcalc(request):
    htmltemplate = get_template('taxcalc.html')
    paramdict = {
        'calcresult' : calculatetax(request),
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)

def calculatetax(request):
    starttax = request.GET.get('starttax','0')
    socials = request.GET.get('socials','0')
    salary = request.GET.get('salary','0')
    taxtype = request.GET.get('type','0')
    print "====================="
    print starttax, socials, salary, taxtype
    print "====================="
    return "wait for input"