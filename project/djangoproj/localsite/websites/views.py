# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import logging
logger = logging.getLogger('localsite')

import datetime
from websites.views import *
from localsite.decorators import (
    valid_params,
)

def websites(request):
    htmltemplate = get_template('websites.html')
    paramdict = {
        'weblist' : getOrderedWebList(),
    }
    html = htmltemplate.render(Context(paramdict))
    return HttpResponse(html)

@valid_params
def webedit(request, operation, param):
    logger.debug("operation: %s %s" % (operation, param))
    if operation == 'delete':
        deleteWebsiteBySeq(param)
    elif operation == 'clear':
        clearWebsites()
    else:
        return HttpResponseRedirect('/error/')
    return HttpResponseRedirect('/websites/')
