import os
from _baseexecuteoperate import *

testDir = os.getcwd()
testDstDir = os.path.join(testDir, "test")
testCopyDir = os.path.join(testDir, "copy")
testFileName = "test.ttf"
testFile = os.path.join(testDir, testFileName)
testFileList = [testFile]
searchList = [r'2345', r'abc']
filePtnList = [r'\.ttf']
testContent = "\
1234567890\n12345\n\
0987654321\n67890\n\
abcdefghijklm\n\
nopqrstuvwxyz\n\
"

def test_getFileContentInStr():
    getFileContentInStr(testFile)

def test_getFileContentInList():
    getFileContentInList(testFile)

def test_getSearchedLineListInFile():
    getSearchedLineListInFile(testFile, searchList)

def test_outputContentToFile():
    outputContentToFile(testDir, testFileName, testContent)

def test_checkSearchedPatternsInFile():
    checkSearchedPatternsInFile(testFile, searchList)

def test_getSearchedFilesInDirWithAbsPath():
    getSearchedFilesInDirWithAbsPath(testDir, filePtnList)

def test_copyListedFileToDir():
    copyListedFileToDir(testDstDir, testFileList)

def test_copyWholeDirContent():
    copyWholeDirContent(testDstDir, testCopyDir)

def test_removeWholeDir():
    removeWholeDir(testDstDir)
    removeWholeDir(testCopyDir)

def test_runExecuteCommand():
    runExecuteCommand(testDir, 'rm %s' % testFileName)

if __name__ == "__main__":
    test_outputContentToFile()
    test_getFileContentInStr()
    test_getFileContentInList()
    test_getSearchedLineListInFile()
    test_checkSearchedPatternsInFile()
    test_getSearchedFilesInDirWithAbsPath()
    test_copyListedFileToDir()
    test_copyWholeDirContent()
    raw_input()
    test_removeWholeDir()
    test_runExecuteCommand()
