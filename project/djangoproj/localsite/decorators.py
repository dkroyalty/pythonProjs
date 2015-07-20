# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

import re
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

