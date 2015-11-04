# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('localsite')

from websites.views import *
from localsite.decorators import *

@std_render_html
def websites(request):
    retdict = {
        'template'  :   'websites.html',
        'paramdict' :   {
                            'weblist' : getOrderedWebList(),
                        },
    }
    return retdict

@valid_params
@std_redirect_url
def webedit(request, operation, param):
    logger.debug("operation: %s %s" % (operation, param))
    if operation == 'delete':
        deleteWebsiteBySeq(param)
    elif operation == 'clear':
        clearWebsites()
    else:
        return '/error/'
    return '/websites/'
