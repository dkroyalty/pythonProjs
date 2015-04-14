import os

_DEBUG_NONE = 0
_DEBUG_BASIC = 1
_DEBUG_DETAIL = 2
_debugLogLevel = _DEBUG_BASIC

def _setloglevel(logLevel):
    if logLevel in [_DEBUG_NONE, _DEBUG_BASIC, _DEBUG_DETAIL]:
        _debugLogLevel = logLevel
        print "sys: set log level: %d" % (_debugLogLevel)

def _printinput(func, *args):
    if _debugLogLevel == _DEBUG_NONE:
        return
    if _debugLogLevel == _DEBUG_DETAIL:
        print ">>> func [%s] input:" % (func.__name__)
        print "=== input detail:\n"
        print args
        print ">>> func [%s] input end\n" % (func.__name__)

def _printoutput(func, obj):
    if _debugLogLevel == _DEBUG_NONE:
        return
    print ">>> func [%s] output:" % (func.__name__)
    if isinstance(obj, str):
        print "=== output string:\n%s" % (obj)
    elif isinstance(obj, int):
        print "=== output integer:\n%d" % (obj)
    elif isinstance(obj, list):
        print "=== output list:\n%d" % (len(obj))
        if _debugLogLevel == _DEBUG_DETAIL:
            print obj
    elif isinstance(obj, dict):
        print "=== output dict:\n%d" % (len(obj.keys()))
        if _debugLogLevel == _DEBUG_DETAIL:
            print obj
    else:
        print "=== output not recognized"
        print type(obj)
    print ">>> func [%s] output end\n" % (func.__name__)

def checkinoutinfo(func):
     def becheckedfunc(*args):
        _printinput(func, args)
        ret = func(*args)
        _printoutput(func, ret)
        return ret
     return becheckedfunc
