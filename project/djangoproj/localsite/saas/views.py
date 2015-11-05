# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

import datetime
import re
from saas.views import *
from localsite.decorators import *

@std_render_html
def taxCalc(request):
    retdict = {
        'template'  :   'taxcalc.html',
        'paramdict' :   calculateTax(request),
    }
    return retdict

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

@std_render_html
def placeDisp(request):
    retdict = {
        'template'  :   'placedisp.html',
        'paramdict' :   buildDispPlace(request),
    }
    return retdict

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

@std_render_html
def placeEdit(request):
    paramdict = dict()
    paramdict = buildPlaceDict()
    retdict = {
        'template'  :   'placeedit.html',
        'paramdict' :   paramdict,
    }
    return retdict

@std_redirect_url
def placeEditConfirm(request):
    placeid = request.GET.get('placeid', None)
    placename = request.GET.get('placename', None)
    placeimg = request.GET.get('placeimg', None)
    imgrect = request.GET.get('imgrect', None)
    desc = request.GET.get('placedesc', None)
    choice = request.GET.get('choice', None)
    imgfile = request.GET.get('imgfile', None)
    if imgfile is not None:
        placeimg = imgfile
    if choice is None:
        pass
    elif choice in ['update', 'create']:
        setPlaceData(placeid, placename, placeimg, imgrect, desc)
    elif choice == 'delete':
        print "delete place"
        print placeid
        deletePlaceData(placeid)
    else:
        print "unrecognized choice:"
        print choice
    return "/saas/place/edit"

def buildPlaceDict(placeid=None):
    placedict = dict()
    placedata = getPlaceData()
    if placedata is None:
        return placedict
    if len(placedata) > 0:
        placedict['placelist'] = placedata
    return placedict

@std_render_html
def itemEdit(request):
    initItemTypeData()
    initItemStatusData()
    paramdict = dict()
    edititem = request.GET.get('edititem', None)
    paramdict = dict()
    if edititem is None:
        paramdict = buildItemDict()
    else:
        itemid = int(convertEquation(edititem))
        paramdict = buildItemDict(itemid)
    retdict = {
        'template'  :   'itemedit.html',
        'paramdict' :   paramdict,
    }
    return retdict

def buildItemDict(itemid=None):
    itemdict = dict()
    itemdata = getItemData()
    if itemdata is None:
        return itemdict
    if len(itemdata) > 0:
        itemdict['itemlist'] = itemdata
        jsData = '|'.join([item.toJsData() for item in itemdata])
        itemdict['jsData'] = jsData
    itemdict['typelist'] = getItemType()
    itemdict['statuslist'] = getItemStatus()
    return itemdict

@std_redirect_url
def itemEditConfirm(request):
    itemname = request.GET.get('itemname', None)
    itemimg = request.GET.get('itemimg', None)
    itemtype = request.GET.get('itemtype', None)
    status = request.GET.get('itemstatus', None)
    desc = request.GET.get('itemdesc', None)
    choice = request.GET.get('choice', "update")
    imgfile = request.GET.get('imgfile', None)
    itemid = request.GET.get('itemid', None)
    if imgfile is not None:
        itemimg = imgfile
    if choice != "update":
        setItemData(itemname, itemimg, itemtype, status, desc)
    else:
        updateItemData(itemid, itemname, itemimg, itemtype, status, desc)
    return "/saas/item/edit"

@std_redirect_url
def itemEditType(request):
    typeid = request.GET.get('typeid', None)
    typename = request.GET.get('typename', None)
    choice = request.GET.get('choice', None)
    if typename is None:
        return "/saas/item/edit"
    if choice is None:
        pass
    elif choice == "update":
        if typeid is None:
            return "/saas/item/edit"
        updateItemType(typeid, typename)
    elif choice == "create":
        setItemType(typename)
    return "/saas/item/edit"

@std_redirect_url
def itemEditStatus(request):
    statusid = request.GET.get('statusid', None)
    statusname = request.GET.get('statusname', None)
    choice = request.GET.get('choice', None)
    if statusname is None:
        return "/saas/item/edit"
    if choice is None:
        pass
    elif choice == "update":
        if statusid is None:
            return "/saas/item/edit"
        updateItemStatus(statusid, statusname)
    elif choice == "create":
        setItemStatus(statusname)
    return "/saas/item/edit"
