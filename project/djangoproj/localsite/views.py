# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('localsite')

from websites.views import *
from localsite.decorators import *

@std_render_html
def index(request):
    retdict = {
        'template' : 'index.html',
        'paramdict' : dict(),
    }
    return retdict

@std_render_html
def error(request):
    retdict = {
        'template'  :   'error.html',
        'paramdict' :   {
                            'redirect' : '/',
                            'staytime' : 10,
                        },
    }
    return retdict
