# -*- coding: utf-8 -*-
import sys
import os
import re
from pyquery import PyQuery

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

def LoadProxySourceUrl(count):
    url = "http://www.proxy.com.ru/list_%d.html" % count
    print url
    htmlcontent = PyQuery(url)
    return htmlcontent

def GetProxyListFromContent(htmlcontent):
    tmplist = [i.text() for i in htmlcontent.items('td')]
    proxylist = []
    for i,tmp in enumerate(tmplist):
        if re.search(r'^\d+\.\d+\.\d+\.\d+$', tmp):
            proxyurl = "%s:%s\t%s" % (tmp, tmplist[i+1], tmplist[i+2])
            proxylist.append(proxyurl)
    return proxylist

def GetAllPageProxyList(totalcount):
    proxylist = []
    if totalcount < 1:
        return proxylist
    for i in range(0, totalcount, 1):
        content = LoadProxySourceUrl(i+1)
        proxylist.extend(GetProxyListFromContent(content))
    return proxylist

if __name__ == "__main__":
    proxylist = GetAllPageProxyList(9)
    outputcontent = "\n".join(proxylist)
    printContentToFile(os.getcwd(), "proxy.txt", outputcontent)
