# -*- coding: utf-8 -*-
import sys
import os
import re
from CareerWebBrowser import CareerWebBrowser

reload(sys)
sys.setdefaultencoding('utf-8')

class CupdataWebBrowser(CareerWebBrowser):
    """ China UnionPay Data """

    def __init__(self):
        super(CupdataWebBrowser, self).__init__()
        self.baseurl = "http://cupdata.zhiye.com/social/"
        self.LoadAllPossibleWebSite()

    def LoadAllPossibleWebSite(self):
        htmlinfo = self.GetUrlPyQueryData(self.baseurl)
        assert htmlinfo is not None
        try:
            footer = htmlinfo('div').filter('.tablefooter')
            pagestr = footer.find('span').eq(0).text()
            searchrst = re.search(r'(\d+)[ ]*\/[ ]*(\d+)', pagestr)
            if searchrst:
                maxpage = searchrst.group(2)
                for index in range(int(maxpage)):
                    addinfo = "?PageIndex=%d" % (index+1)
                    self.AddAssignedWebsite(addinfo, "社会招聘页面%d" % (index+1))
        except:
            assert False

    def GatherCareerInfoFromWebContent(self, infostr):
        super(CupdataWebBrowser, self).GatherCareerInfoFromWebContent(infostr)
        tabletrlist = self.GatherCupDataCareerInfo(infostr)
        assert tabletrlist is not None
        self.GetCareerInfoFromTable(tabletrlist)

    def GatherCupDataCareerInfo(self, htmlinfo):
        if htmlinfo is None:
            print "Error: html content is None"
            return None
        tablelist = htmlinfo('table').filter('.listtable')
        tabletrlist = tablelist.find('tr')
        return tabletrlist

    def GetCareerInfoFromTable(self, tabletrlist):
        counter = 0
        while True:
            trpart = tabletrlist.eq(counter)
            if len(trpart) == 0:
                break
            link = trpart('a').attr('href') if trpart.find('a') else ""
            counter += 1
            if "上海" in trpart.text():
                prevurl = "http://cupdata.zhiye.com/"
                outputstr = "\t%s\t%s%s" % (trpart.text(), prevurl, link)
                self.AddToOutputInfo(outputstr)
