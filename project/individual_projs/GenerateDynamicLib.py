# -*- coding: utf-8 -*-
import os
import re
import sys
import argparse
import subprocess
from os import path as ospath

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf8')

def BuildSourceFile(filepath):
    print "build file: %s" % filepath
    assert ospath.isfile(filepath)
    content = getFileContentInStr(filepath)
    content = AddHeaderFileDeclare(content)
    filename = re.sub(r'\..*?$', '', ospath.basename(filepath))
    funcinfolist = GatherAllFunction(content)
    content += '\n\n'
    for eachfunc in funcinfolist:
        content += GeneratePackageFunction(eachfunc, filename)
    content += BuildMethodDef(funcinfolist, filename)
    outputdir = ospath.dirname(filepath)
    outputname = 'out_%s' % (ospath.basename(filepath))
    outputContentToFile(ospath.join(outputdir, outputname), content)
    setfile = BuildSetupFile(outputdir, filename, outputname)
    cmd = 'sudo python %s install' % (setfile)
    runExecuteCommand(outputdir, cmd)

def AddHeaderFileDeclare(filecontent):
    pattern = r'#include.*?Python\.h.*?\n'
    if re.search(pattern, filecontent):
        filecontent = re.sub(pattern, '', filecontent)
    return '#include "Python.h"\n%s' % (filecontent)

def GatherAllFunction(filecontent):
    funcpattern = r'\n[ ]*([^;=}\r\n ]+[* ]+)([^;= ]+?)\(([^;]*?)\)'
    funcdata = re.findall(funcpattern, filecontent)
    for info in funcdata:
        if info[1].strip().lower() == 'main':
            funcdata.remove(info)
    return funcdata

def GatherArgsInfo(argdata):
    arglist = argdata.split(',')
    infolist = [re.sub(r'[^ ]$', '', x.strip()) for x in arglist]
    return infolist

def ConvertCommonCode(sourcetype):
    convertlist = [
        (r'char[ ]*\*', 's'),
        (r'string', 's'),
        (r'int', 'i'),
        (r'long', 'l'),
        (r'char', 'c'),
        (r'double', 'd'),
        (r'void', ''),
    ]
    for eachtup in convertlist:
        if re.search(eachtup[0], sourcetype):
            return eachtup[-1]
    return ''

def GeneratePackageFunction(funcinfo, prename):
    initstr = 'static PyObject * Ex%s_%s(PyObject *self, PyObject *args) {\n' %\
            (prename, funcinfo[1])
    typelist = GatherArgsInfo(funcinfo[-1])
    paramstr = ''
    parsetypes = []
    parseparams = []
    callparams = []
    for i, typename in enumerate(typelist):
        paramstr += '\t%s param%d;\n' % (typename.strip(), i)
        parsetypes.append(ConvertCommonCode(typename))
        parseparams.append('&param%d' % (i))
        callparams.append('param%d' % (i))
    callstart = '\tif (!(PyArg_ParseTuple(args, "%s", %s))) {\n' % \
            (''.join(parsetypes), ', '.join(parseparams))
    callend = '\t\treturn NULL;\n\t}\n'
    returnstr = '\treturn (PyObject *)Py_BuildValue("%s", %s(%s));\n}\n' % \
            (ConvertCommonCode(funcinfo[0]), funcinfo[1], ', '.join(callparams))
    totalstr = '%s%s%s%s%s' % (initstr, paramstr, callstart, callend, returnstr)
    return totalstr

def BuildMethodDef(funcinfolist, prename):
    defstr = 'static PyMethodDef \nEx%sMethods[] = {\n' % (prename)
    contentstr = ''
    for eachfunc in funcinfolist:
        contentstr += '\t{"%s", Ex%s_%s, METH_VARARGS},\n' % \
                (eachfunc[1], prename, eachfunc[1])
    defendstr = '\t{NULL, NULL},\n};\n'
    initstr = 'void initEx%s() {\n\tPy_InitModule("Ex%s", Ex%sMethods);\n}\n' %\
            (prename, prename, prename)
    totalstr = '%s%s%s%s' % (defstr, contentstr, defendstr, initstr)
    return totalstr

def BuildSetupFile(outputpath, prename, generatedfile):
    contentstr = ''
    contentstr += '#!/usr/bin/env python\n'
    contentstr += 'from distutils.core import setup, Extension\n'
    contentstr += 'MOD = \'Ex%s\'\n' % prename
    contentstr += 'setup(name=MOD, '
    contentstr += 'ext_modules=[Extension(MOD, sources=[\'%s\'])])\n' % \
            (generatedfile)
    outputname = 'setupEx%s.py' % prename
    outputContentToFile(ospath.join(outputpath, outputname), contentstr)
    return outputname

def CompileSourceFile(filepath):
    print "compile file: %s" % filepath
    filename = re.sub(r'\..*?$', '.so', ospath.basename(filepath))
    outfile = ospath.join(ospath.dirname(filepath), filename)
    cmd = 'gcc %s -o %s' % (filepath, outfile)
    runExecuteCommand(ospath.dirname(filepath), cmd)

def LoadParamArguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--source',
        dest='sourcefile', help='source operate file')
    argparser.add_argument('-o', '--operate',
        dest='operation', help='operation for source')
    args = argparser.parse_args()
    paramdict = dict()
    paramdict['sourcefile'] = getattr(args, 'sourcefile', None)
    paramdict['operation'] = getattr(args, 'operation', None)
    return paramdict

def DistributeOperation(paramdict):
    assert isinstance(paramdict, dict) is True
    sourcefile = ospath.abspath(paramdict['sourcefile'])
    assert ospath.isfile(sourcefile)
    operation = paramdict['operation']
    if sourcefile is None or operation is None:
        print >> sys.stderr, u'lack source or operation'
        return
    operationdict = {
        'build' : "BuildSourceFile(sourcefile)",
        'compile' : "CompileSourceFile(sourcefile)",
    }
    if operation in operationdict.keys():
        eval(operationdict[operation])

if __name__ == "__main__":
    try:
        paramdict = LoadParamArguments()
        DistributeOperation(paramdict)
    except:
        print >> sys.stderr, u'fail to operate'
        raise
