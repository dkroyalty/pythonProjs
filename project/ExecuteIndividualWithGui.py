# -*- coding: utf-8 -*-
import sys
import os
import shutil
from Tkinter import *
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

class GUI_Execute():

    FRAME_CONTAINS_COUNT = 5
    WINDOWS_SIZE_WIDTH = 640
    WINDOWS_SIZE_HEIGHT = 320

    def __init__(self, workPath):
        self.workPath = workPath
        self.frameStartCnt = 0
        self.executeFile = ""
        self.description = ""

    def initExecuteFiles(self):
        ptnList = [r'^[^.|_].*\.py$']
        commentPtnList = [r'^\#Comment:.*$']
        paramPtnList = [r'^\#Param:.*$']
        fileList = getSearchedFilesInDirWithAbsPath(self.workPath, ptnList)
        self.executeDict = dict()
        for eachfile in fileList:
            commentList = getSearchedLineListInFile(eachfile, commentPtnList)
            comment = re.sub(r'^\#Comment:', '', ''.join(commentList))
            paramList = getSearchedLineListInFile(eachfile, paramPtnList)
            paramNum = 0
            if len(paramList) > 0:
                paramNum = re.sub(r'^\#Param:', '', paramList[0])
            self.executeDict[os.path.basename(eachfile)] = [comment, paramNum]

    def checkExecuteDict(self):
        for eachkey in self.executeDict.keys():
            print eachkey
            print self.executeDict[eachkey]

    def createGuiWindows(self):
        self.root = Tk()
        self.root.minsize(self.WINDOWS_SIZE_WIDTH, self.WINDOWS_SIZE_HEIGHT)
        self.root.maxsize(self.WINDOWS_SIZE_WIDTH, self.WINDOWS_SIZE_HEIGHT)
        self.frame = Frame(self.root)
        self.pyList = self.executeDict.keys()
        self.pyList.sort()

    def activeGuiWindows(self):
        self.root.mainloop()

    def getFrameInWindow(self):
        frame = Frame(self.root)
        frame.place(anchor=W, \
                relx=0, rely=0.5, \
                relwidth = 1.0, relheight = 1.0)
        return frame

    def flushCurrentFrame(self, frame):
        if self.frame:
            self.frame.destroy()
        self.frame = frame

    def buildRangeButtonFrame(self, frame, startNum, endNum):
        if startNum >= len(self.pyList):
            return
        if endNum > len(self.pyList):
            endNum = len(self.pyList)
        for i in range(startNum, endNum):
            colBtn = Button(frame, text=self.pyList[i], \
                command=lambda count=i: self.executePyBtn(count))
            colBtn.place(anchor=W, bordermode=OUTSIDE, \
                relx=0, rely=0.08 + 0.16*(i-startNum), \
                relwidth = 1.0, relheight = 0.16)
        prevBtn = Button(frame, text="PREV", command=self.buildPrevRangeFrame)
        prevBtn.place(anchor=W, bordermode=OUTSIDE, \
            relx=0, rely=0.9, \
            relwidth = 0.2, relheight = 0.2)
        postBtn = Button(frame, text="POST", command=self.buildPostRangeFrame)
        postBtn.place(anchor=W, bordermode=OUTSIDE, \
            relx=0.8, rely=0.9, \
            relwidth = 0.2, relheight = 0.2)

    def executePyBtn(self, count):
        self.executeFile = os.path.join(self.workPath, self.pyList[count])
        self.description = self.executeDict[self.pyList[count]][0]
        self.paramNumber = self.executeDict[self.pyList[count]][1]
        if os.path.isfile(self.executeFile):
            print self.executeFile
            print self.description
            self.createFunctionExecuteFrame()

    def buildPrevRangeFrame(self):
        if self.frameStartCnt - self.FRAME_CONTAINS_COUNT >= 0:
            self.frameStartCnt -= self.FRAME_CONTAINS_COUNT
            self.createBasicFrame()

    def buildPostRangeFrame(self):
        if self.frameStartCnt + self.FRAME_CONTAINS_COUNT < len(self.pyList):
            self.frameStartCnt += self.FRAME_CONTAINS_COUNT
            self.createBasicFrame()

    def createBasicFrame(self):
        self.executeFile = ""
        dispRange = self.frameStartCnt+self.FRAME_CONTAINS_COUNT
        frame = self.getFrameInWindow()
        self.buildRangeButtonFrame(frame, self.frameStartCnt, dispRange)
        self.flushCurrentFrame(frame)

    def createFunctionExecuteFrame(self):
        frame = self.getFrameInWindow()
        intro = Label(frame, text=self.description)
        intro.place(anchor=N, bordermode=OUTSIDE, \
            relx=0.5, rely=0.05, \
            relwidth = 0.8, relheight = 0.2)
        entryLabel = Label(frame, text="Param")
        entryLabel.place(anchor=N, bordermode=OUTSIDE, \
            relx=0.5, rely=0.25, \
            relwidth = 0.2, relheight = 0.1)
        self.paramList = []
        for i in range(0, int(self.paramNumber)):
            entryParam = Entry(frame, justify=LEFT)
            entryParam.place(anchor=N, bordermode=OUTSIDE, \
                relx=0.5, rely=0.35 + 0.10*i, \
                relwidth = 0.5, relheight = 0.1)
            self.paramList.append(entryParam)
        executeBtn = Button(frame, text="Execute", command=self.runSelectFunction)
        executeBtn.place(anchor=N, bordermode=OUTSIDE, \
            relx=0.25, rely=0.9, \
            relwidth = 0.2, relheight = 0.1)
        backBtn = Button(frame, text="Back", command=self.createBasicFrame)
        backBtn.place(anchor=N, bordermode=OUTSIDE, \
            relx=0.75, rely=0.9, \
            relwidth = 0.2, relheight = 0.1)
        self.flushCurrentFrame(frame)

    def runSelectFunction(self):
        paramStr = ""
        for eachParam in self.paramList:
            paramStr += " '%s'" % eachParam.get()
        cmdStr = "python %s %s" % (self.executeFile, paramStr)
        print cmdStr
        runExecuteCommand(self.workPath, cmdStr)

if __name__ == "__main__":
    runner = GUI_Execute(os.path.join(os.getcwd(), "individual_projs"))
    runner.initExecuteFiles()
    runner.checkExecuteDict()
    runner.createGuiWindows()
    runner.createBasicFrame()
    runner.activeGuiWindows()

