# -*- coding: utf-8 -*-
import sys
import os
import time
from CmbWebBrowser import CmbWebBrowser
from CupdataWebBrowser import CupdataWebBrowser

sys.path.append("../..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

def GetDifferentBankInfo():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timeinfo = "============= [%s] =============" % (timestamp)
    print timeinfo
    return
    cupdatainfo = CupdataWebBrowser().GatherBankCareerInfo()
    print cupdatainfo
    cmbinfo = CmbWebBrowser().GatherBankCareerInfo()
    print cmbinfo

if __name__ == "__main__":
    GetDifferentBankInfo()
