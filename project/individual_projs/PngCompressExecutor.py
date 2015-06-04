# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import threading
import time
from PIL import Image

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

_toolPath = os.path.join(os.getcwd(), "../../tools/pngquant/pngquant")
_showDetail = False

#Comment:compress png file with pngquant
#Param:1
class checker(threading.Thread):
    def __init__(self, interval=1):
        threading.Thread.__init__(self)
        self.interval = interval
        self.thread_stop = False
        self.checkPairList = []
 
    def insertPair(self, insertCheckPair):
        self.checkPairList.append(insertCheckPair)

    def getRunningSize(self):
        return len(self.checkPairList)

    def run(self):
        while True:
            rmNumList = []
            for num, eachPair in enumerate(self.checkPairList):
                retVal = subprocess.Popen.poll(eachPair[0])
                if retVal == 0:
                    #print "%s process success" % (eachPair[1])
                    rmNumList.append(num)
                elif retVal is None:
                    pass
                else:
                    print "########## error code %d ##########" % (retVal)
                    print "|- %s" % (eachPair[1])
                    rmNumList.append(num)
            if len(rmNumList) > 0:
                rmNumList.reverse()
                for eachNum in rmNumList:
                    del self.checkPairList[eachNum]
            if self.thread_stop and len(self.checkPairList) == 0:
                break
            time.sleep(self.interval)
        print "check thread close"

    def stop(self):
        self.thread_stop = True

def ConvertPicture(pictureList, limitNum=500, interval=1, bitSize=256):
    checkThread = checker()
    checkThread.start()
    executeCnt = 0
    skipCnt = 0
    cannotReadList = []
    print "total execute file : %d" % (len(pictureList))
    while len(pictureList) > 0:
        while checkThread.getRunningSize() < limitNum:
            if len(pictureList) > 0:
                picFullPath = pictureList.pop()
                try:
                    im = Image.open(picFullPath)
                    colorCnt = 0
                    if im.getcolors():
                        colorCnt = len(im.getcolors())
                except:
                    cannotReadList.append(picFullPath)
                    continue
                if colorCnt <= bitSize and colorCnt > 0:
                    skipCnt += 1
                else:
                    executeCnt += 1
                    checkThread.insertPair(ExcuteQuantPic(picFullPath))
            else:
                break
        time.sleep(interval)
    checkThread.stop()
    print "execute file : %d" % (executeCnt)
    print "skip file : %d" % (skipCnt)
    print "connot read : %d" % (len(cannotReadList))
    if _showDetail == True:
        for eachFile in cannotReadList:
            print eachFile

def ExcuteQuantPic(picFullPath, bitSize=256):
    cmdStr = "%s --ext .png -f %d -- \"%s\"" % (_toolPath, bitSize, picFullPath)
    runprocess = subprocess.Popen(cmdStr, shell=True)
    return [runprocess, picFullPath]

def CompressPngFilesInDir(dirPath):
    pictureList = getSearchedFilesInDirWithAbsPath(dirPath, [r'\.png$'])
    if len(pictureList) > 0:
        ConvertPicture(pictureList)

if __name__ == "__main__":
    param = ""
    if len(sys.argv) > 1:
        param = sys.argv[1]
    assert os.path.isdir(param)
    CompressPngFilesInDir(param)
