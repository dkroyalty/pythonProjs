# -*- coding: utf-8 -*-
import sys
import os
from pyquery import PyQuery

sys.path.append("..")
sys.path.append("../..")
import UrlConnection

reload(sys)
sys.setdefaultencoding('utf-8')

class CareerWebBrowser(object):
    """ basic class for gathering bank info from related website """

    def __init__(self):
        self.baseurl = None
        self.assignedlist = []
        self.outputinfo = ""

    def AddAssignedWebsite(self, website, describe):
        if self.baseurl is None:
            self.assignedlist.append([website, describe])
        else:
            absoluteurl = os.path.join(self.baseurl, website)
            self.assignedlist.append([absoluteurl, describe])
        
    def GetUrlPyQueryData(self, urlsite):
        content = UrlConnection.LoadUrlContent(urlsite)
        searchrst = None
        if content is not None:
            searchrst = PyQuery(content)
        return searchrst

    def AddToOutputInfo(self, outputstr):
        self.outputinfo = "%s\n%s" % (self.outputinfo, outputstr)

    def GatherBankCareerInfo(self):
        for webpair in self.assignedlist:
            self.AddToOutputInfo("\n>>>%s" % ("\t".join(webpair)))
            infopart = self.GetUrlPyQueryData(webpair[0])
            self.GatherCareerInfoFromWebContent(infopart)
        return self.outputinfo

    def GatherCareerInfoFromWebContent(self, infostr):
        pass
