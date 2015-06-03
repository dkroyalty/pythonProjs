# -*- coding: utf-8 -*-
import sys
import os
import re
import random
import socket
import urllib
import urllib2
import cookielib

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

urllib2.socket.setdefaulttimeout(10)

def GetTotalProxyList():
    filepath = os.path.join(os.getcwd(), "proxy.txt")
    originlist = getFileContentInList(filepath)
    proxylist = []
    for ippair in originlist:
        ip = ippair.split("\t")[0]
        ipdict = dict()
        ipdict["http"] = "http://%s"%ip
        proxylist.append(ipdict)
    return proxylist

def GetGeneratedCookie():
    cookie = cookielib.CookieJar()
    cookiehandler = urllib2.HTTPCookieProcessor(cookie)
    return cookiehandler

def GetRandomAgent():
    useragentlist = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
    ]
    useragent = random.choice(useragentlist)
    #print useragent
    return useragent

def LoadUrlContent(urlSite, proxyip=None):
    useragent = GetRandomAgent()
    if proxyip is None:
        openerparamlist = [urllib2.HTTPHandler]
        openerparamlist.append(urllib2.ProxyHandler(proxyip))
        openerparamlist.append(GetGeneratedCookie())
        opener = urllib2.build_opener(*openerparamlist)
        urllib2.install_opener(opener)
    request = urllib2.Request(urlSite)
    request.add_header('User-Agent',useragent)
    urlhtml = None
    # soemthing strange happened when call urlopen
    # some exception raised in "data = self._sock.recv(self._rbufsize)"
    # the last output is "socket.timeout: timed out"
    # sometimes output "socket.error: [Errno 54] Connection reset by peer"
    # however the exception not caught in try...except...
    try:  
        urlhtml = urllib2.urlopen(request).read()
    except urllib2.URLError, e:  
        if isinstance(e.reason, socket.timeout):
            print "Error: Time Out"
        else:
            print "Error: %r" % e
    return urlhtml

if __name__ == "__main__":
    #param = "http://www.baidu.com"
    param = "http://www.google.com"
    if len(sys.argv) > 1:
        param = sys.argv[1]
    proxylist = GetTotalProxyList()
    while len(proxylist) > 0:
        proxyip = random.choice(proxylist)
        proxylist.remove(proxyip)
        print proxyip
        content = LoadUrlContent(param, proxyip)
        if content is not None:
            print content
            break
