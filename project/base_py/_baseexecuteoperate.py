import os
import re
import shutil
import subprocess
from _basedecorators import *
from _basecheckoperate import *

@checkinoutinfo
def getFileContentInStr(sourceFile):
    checklegalfile(sourceFile)
    with open(sourceFile, 'rb') as fileHandler:
        fileContent = fileHandler.read()
    return fileContent

@checkinoutinfo
def getFileContentInList(sourceFile):
    checklegalfile(sourceFile)
    contentList = []
    with open(sourceFile, 'rb') as fileHandler:
        contents = fileHandler.readlines()
    for eachLine in contents:
        lineCont = re.sub(r'\n$', '', eachLine)
        lineCont = lineCont.lstrip()
        if len(lineCont) > 0:
            contentList.append(lineCont)
    return contentList

@checkinoutinfo
def getSearchedLineListInFile(sourceFile, searchList=[]):
    contentList = getFileContentInList(sourceFile)
    rstList = []
    for eachLine in contentList:
        if len(searchList) > 0:
            for eachPtn in searchList:
                if re.search(eachPtn, eachLine):
                    rstList.append(eachLine)
                    break
    return rstList

@checkinoutinfo
def outputContentToFile(outputDir, outputFileName, outputContent):
    checklegaldir(outputDir)
    outputFile = os.path.join(outputDir, outputFileName)
    with open(outputFile, 'wb') as fileHandler:
        fileHandler.write(outputContent)
    return "output to %s end" % (outputFile)

@checkinoutinfo
def checkSearchedPatternsInFile(sourceFile, checkPtnList=[]):
    content = getFileContentInStr(sourceFile)
    for eachPtn in checkPtnList:
        if re.search(eachPtn, content):
            return True
    return False

@checkinoutinfo
def getSearchedFilesInDirWithAbsPath(sourceDir, searchPtnList, beLoop=True):
    checklegaldir(sourceDir)
    fileList = []
    for eachFile in os.listdir(sourceDir):
        absPath =  os.path.join(sourceDir, eachFile)
        if os.path.isfile(absPath):
            if len(searchPtnList) > 0:
                for eachPtn in searchPtnList:
                    if re.search(eachPtn, eachFile):
                        fileList.append(absPath)
                        break
            else:
                fileList.append(absPath)
        elif os.path.isdir(absPath) and beLoop == True:
            fileList.extend(getSearchedFilesInDirWithAbsPath(absPath, searchPtnList))
    return fileList

@checkinoutinfo
def copyListedFileToDir(dstDir, fileList):
    checkormakedir(dstDir)
    for eachFile in fileList:
        fileName = os.path.basename(eachFile)
        dstPath = os.path.join(dstDir, fileName)
        if os.path.isfile(eachFile):
            copyFileToDst(eachFile, dstPath)

@checkinoutinfo
def copyWholeDirContent(sourceDir, dstDir, beCover=True):
    checkormakedir(dstDir)
    for eachFile in os.listdir(sourceDir):
        absPath =  os.path.join(sourceDir, eachFile)
        dstPath = os.path.join(dstDir, eachFile)
        if os.path.isfile(absPath):
            copyFileToDst(absPath, dstPath, beCover)
        elif os.path.isdir(absPath):
            if os.path.isdir(dstPath) and beCover == True:
                removeWholeDir(absPath)
                os.mkdir(dstPath)
            copyWholeDirContent(absPath, dstPath, beCover)

@checkinoutinfo
def copyFileToDst(sourceFile, dstFile, beCover=True):
    checklegalfile(sourceFile)
    if re.search(r'^\.', os.path.basename(sourceFile)):
        return False
    if os.path.isfile(dstFile):
        if beCover == True:
            shutil.copy(sourceFile, dstFile)
        else:
            return False
    else:
        checkormakedir(os.path.dirname(dstFile))
        shutil.copy(sourceFile, dstFile)
    return True

@checkinoutinfo
def removeWholeDir(absPath):
    checklegaldir(absPath)
    for eachCont in os.listdir(absPath):
        subPath = os.path.join(absPath, eachCont)
        if os.path.isfile(subPath):
            os.remove(subPath)
        elif os.path.isdir(subPath):
            removeWholeDir(subPath)
            os.rmdir(subPath)
    os.rmdir(absPath)
    return "remove dir: %s" % absPath

@checkinoutinfo
def runExecuteCommand(executeDir, runCommand):
    checklegaldir(executeDir)
    prevDir = os.getcwd()
    os.chdir(executeDir)
    runner = subprocess.Popen(runCommand, shell=True, stdout = subprocess.PIPE)
    runner.wait()
    runResult = runner.stdout.read()
    os.chdir(prevDir)
    return runResult

@checkinoutinfo
def printContentToFile(outputDir, outputFileName, outputContent):
    checklegaldir(outputDir)
    outputFile = os.path.join(outputDir, outputFileName)
    with open(outputFile, 'wb') as fileHandler:
        print >> fileHandler, outputContent
    return "output to %s end" % (outputFile)
