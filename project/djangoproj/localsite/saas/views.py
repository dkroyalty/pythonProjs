# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

import datetime
import re
from saas.views import *
from localsite.decorators import (
    valid_params,
)

def taxcalc(request):
    htmltemplate = get_template('taxcalc.html')
    calcresult = calculatetax(request)
    html = htmltemplate.render(Context(calcresult))
    return HttpResponse(html)

def calculatetax(request):
    starttax = request.GET.get('starttax','0')
    socials = request.GET.get('socials','0')
    salary = request.GET.get('salary','0')
    taxtype = request.GET.get('type','0')
    logger.debug("calctax: %s %s %s %s" % (starttax, socials, salary, taxtype))
    starttax = convertequation(starttax)
    socials = convertequation(socials)
    salary = convertequation(salary)
    if taxtype == '0':
        return "wait for input"
    initDataRecord()
    needtaxpart = float(salary) - float(socials) - float(starttax)
    taxdata = getSuitableStandard(needtaxpart, taxtype=='self')
    selftax = needtaxpart * float(taxdata.taxrate) * 1.0/ 100.0
    selftax -= float(taxdata.taxfastsub)
    calcrst = float(salary) - float(socials) - selftax
    logger.debug("calctax result: %.2f %.2f" % (float(selftax), float(calcrst)))
    rst = dict()
    rst['starttax'] = "%.2f" % (float(starttax))
    rst['socials'] = "%.2f" % (float(socials))
    rst['salary'] = "%.2f" % (float(salary))
    if taxtype == 'other':
        rst['other'] = '1'
    rst['tax'] = "%.2f" % (float(selftax))
    rst['realget'] = "%.2f" % (float(calcrst))
    return rst

def convertequation(equation):
    rst = equation
    if isinstance(equation, unicode) and re.search(r'^\d', equation):
        print "fit cond : %s" % (equation)
        if re.search(r'[\+\-\*\/\(\)]', equation):
            try:
                rst = eval(equation)
            except:
                rst = ''
                print "disable convert equation: %s" % equation
    return rst

