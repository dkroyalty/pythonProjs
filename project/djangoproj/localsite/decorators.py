# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

import re
import datetime
import logging
logger = logging.getLogger('localsite')

def valid_params(func):
    def decorator(request, **args):
        for each in args.keys():
            if args[each] is None:
                logger.error("param %s is None" % each)
                return HttpResponseRedirect('/error/')
        return func(request, **args)
    return decorator

def std_render_html(func):
    def decorator(request, **args):
        rstdict = func(request, **args)
        if isinstance(rstdict, dict):
            if rstdict.has_key('template') and rstdict.has_key('paramdict'):
                htmltemplate = get_template(rstdict['template'])
                if isinstance(rstdict['paramdict'], dict):
                    if not rstdict['paramdict'].has_key('timestamp'):
                        rstdict['paramdict']['timestamp'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
                    html = htmltemplate.render(Context(rstdict['paramdict']))
                    return HttpResponse(html)
                else:
                    print "illegal paramdict"
        return rstdict
    return decorator

def std_redirect_url(func):
    def decorator(request, **args):
        rst = func(request, **args)
        try:
            return HttpResponseRedirect(rst)
        except:
            return HttpResponseRedirect('/error/')
    return decorator
