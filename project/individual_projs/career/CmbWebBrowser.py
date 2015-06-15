# -*- coding: utf-8 -*-
import sys
import os
import re
from CareerWebBrowser import CareerWebBrowser

reload(sys)
sys.setdefaultencoding('utf-8')

class CmbWebBrowser(CareerWebBrowser):
    """ China Merchants Bank """

    def __init__(self):
        super(CmbWebBrowser, self).__init__()
        self.baseurl = "http://career.cmbchina.com/Social/"
        self.AddAssignedWebsite("longterm.aspx?branch=0755", "总行长期社招")
        self.AddAssignedWebsite("longterm.aspx?branch=0021", "上海分行长期社招")
        self.AddAssignedWebsite("default.aspx?branch=0755", "总行社招")
        self.AddAssignedWebsite("default.aspx?branch=0021", "上海分行社招")

    def GatherCareerInfoFromWebContent(self, infostr):
        super(CmbWebBrowser, self).GatherCareerInfoFromWebContent(infostr)
        tabletrlist = self.GatherCMBCareerInfo(infostr)
        assert tabletrlist is not None
        self.GetCareerInfoFromTable(tabletrlist)

    def GatherCMBCareerInfo(self, htmlinfo):
        if htmlinfo is None:
            print "Error: html content is None"
            return None
        poslist = htmlinfo('div').filter('.poslist')
        tabletrlist = poslist('table').find('tr')
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
                outputstr = "\t%s\t%s%s" % (trpart.text(), self.baseurl, link)
                self.AddToOutputInfo(outputstr)
