# -*- coding: utf-8 -*-
import sys
import os
import re
import argparse
from os import path as ospath

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

def ConvertDirFileFormat(dirpath, fileformat, patternlist):
    assert ospath.isdir(dirpath)
    print dirpath
    print fileformat
    print patternlist
    filelist = getSearchedFilesInDirWithAbsPath(dirpath, patternlist)
    for eachfile in filelist:
        ConvertFileFormat(eachfile, fileformat)

def ConvertFileFormat(filepath, fileformat):
    print "exe %s" % filepath
    assert ospath.isfile(filepath)
    content = getFileContentInStr(filepath)
    repcont = content.replace("\r\n", "\n")
    if fileformat.lower() == 'dos':
        repcont = repcont.replace("\n", "\r\n")
    outputContentToFile(filepath, repcont)

def CompareDirFileContent(sourcedir, refdir, patternlist):
    assert ospath.isdir(sourcedir)
    assert ospath.isdir(refdir)
    srclist = getSearchedFilesInDirWithAbsPath(sourcedir, patternlist)
    reflist = getSearchedFilesInDirWithAbsPath(refdir, patternlist)
    CheckNotExistFile(srclist, reflist)

def CheckNotExistFile(srclist, reflist):
    srcset = set([ospath.basename(x) for x in srclist])
    refset = set([ospath.basename(x) for x in reflist])
    cmpset = srcset.difference(refset)
    print cmpset

def GetPartialFileName(filepath, lv=1):
    assert ospath.isfile(filepath)
    filename = ospath.basename(filepath)
    executepath = ospath.dirname(filepath)
    for i in xrange(lv):
        filename = ospath.join(ospath.basename(executepath), filename)
        executepath = ospath.dirname(executepath)
    return filename

def CopyDirContent(srcpath, dstpath, copymode):
    onlyoverwrite = (copymode == 'ow')
    print srcpath, dstpath, copymode
    assert ospath.isdir(srcpath)
    assert ospath.isdir(dstpath)
    srclist = getSearchedFilesInDirWithAbsPath(srcpath)
    reflist = getSearchedFilesInDirWithAbsPath(dstpath)
    operatelist = []
    if onlyoverwrite is True:
        srcset = set([ospath.basename(x) for x in srclist])
        refset = set([ospath.basename(x) for x in reflist])
        duplist = list(srcset.intersection(refset))
        operatelist = [ospath.join(srcpath, x)  for x in duplist]
    else:
        operatelist = srclist
    for filepath in operatelist:
        filename = ospath.basename(filepath)
        if re.search(r'^\.', filename):
            continue
        if ospath.isfile(filepath) is True:
            fulldstpath = ospath.join(dstpath, filename)
            copyFileToDst(filepath, fulldstpath)
            print "execute: %s -> %s" % (filepath, fulldstpath)
    return operatelist

def LoadParamArguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--source',
        dest='sourcedir', help='source directory absolute path')
    argparser.add_argument('-o', '--operate',
        dest='operation', help='operation for source')
    argparser.add_argument('-d', '--detail',
        dest='detail', help='detail information for operation')
    argparser.add_argument('-e', '--extra',
        dest='extra', help='extra information')
    args = argparser.parse_args()
    paramdict = dict()
    paramdict['sourcedir'] = getattr(args, 'sourcedir', None)
    paramdict['operation'] = getattr(args, 'operation', None)
    paramdict['detail'] = getattr(args, 'detail', None)
    paramdict['extra'] = getattr(args, 'extra', None)
    return paramdict

def DistributeOperation(paramdict):
    assert isinstance(paramdict, dict) is True
    sourcedir = paramdict['sourcedir']
    operation = paramdict['operation']
    detail = paramdict['detail']
    extra = paramdict['extra']
    if sourcedir is None or operation is None:
        print >> sys.stderr, u'lack source or operation'
        return
    operationdict = {
        'conv' : "ConvertDirFileFormat(sourcedir, detail, [extra])",
        'comp' : "CompareDirFileContent(sourcedir, detail, [extra])",
        'copy' : "CopyDirContent(sourcedir, detail, extra)",
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
