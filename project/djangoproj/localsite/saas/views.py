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

def taxCalc(request):
    htmltemplate = get_template('taxcalc.html')
    calcresult = calculateTax(request)
    html = htmltemplate.render(Context(calcresult))
    return HttpResponse(html)

def calculateTax(request):
    starttax = request.GET.get('starttax','0')
    socials = request.GET.get('socials','0')
    salary = request.GET.get('salary','0')
    taxtype = request.GET.get('type','0')
    logger.debug("calctax: %s %s %s %s" % (starttax, socials, salary, taxtype))
    starttax = convertEquation(starttax)
    socials = convertEquation(socials)
    salary = convertEquation(salary)
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

def convertEquation(equation):
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

def placeDisp(request):
    htmltemplate = get_template('placedisp.html')
    initPlaceData()
    html = htmltemplate.render(Context(buildDispPlace(request)))
    return HttpResponse(html)

def buildDispPlace(request):
    basicplace = request.GET.get('dispplace', None)
    dispdict = dict()
    placedata = getPlaceData()
    if placedata is None:
        return dispdict
    dispplace = None
    if basicplace is None:
        if len(placedata) > 0:
            dispplace = placedata[0]
            dispdict['basic'] = dispplace
    else:
        basicplace = int(convertEquation(basicplace))
        for eachplace in placedata:
            if basicplace == eachplace.id:
                dispplace = eachplace
                dispdict['basic'] = dispplace
                break
    if dispplace is not None:
        sonplacelist = getRelatedPlaceList(dispplace.id)
        if len(sonplacelist) > 0:
            dispdict['extend'] = sonplacelist
    return dispdict

def buildContainPlace(placeidlist):
    containlist = []
    if len(placeidlist) == 0:
        return containlist
    for eachid in placeidlist:
        placedata = getPlaceData(eachid)
        if placedata is not None:
            containlist.append(placedata)
    return containlist

def placeEdit(request):
    htmltemplate = get_template('placeedit.html')
    editplace = request.GET.get('editplace', None)
    paramdict = dict()
    if editplace is None:
        paramdict = buildPlaceDict()
    else:
        placeid = int(convertEquation(editplace))
        paramdict = buildPlaceDict(placeid)
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)

def placeEditConfirm(request):
    placeid = request.GET.get('placeid', None)
    placename = request.GET.get('placename', None)
    placeimg = request.GET.get('placeimg', None)
    imgrect = request.GET.get('imgrect', None)
    desc = request.GET.get('placedesc', None)
    choice = request.GET.get('choice', "update")
    if choice != "update":
        placeid = None
    setPlaceData(placeid, placename, placeimg, imgrect, desc)
    return HttpResponseRedirect("/saas/place/edit")

def buildPlaceDict(placeid=None):
    placedict = dict()
    placedata = getPlaceData()
    if placedata is None:
        return placedict
    placedict['placelist'] = placedata
    for eachplace in placedata:
        if placeid == eachplace.id:
            placedict['editplace'] = eachplace
            break
    return placedict


