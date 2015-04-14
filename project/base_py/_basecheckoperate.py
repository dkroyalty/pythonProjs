import os

def checklegaldir(dirpath):
    if not os.path.isdir(dirpath):
        print "!!! %s is not legal dir" % (dirpath)
        exit(-1)

def checklegalfile(filepath):
    if not os.path.isfile(filepath):
        print "!!! %s is not legal file" % (filepath)
        exit(-1)

def checkormakedir(dirpath):
    makeparentdir(dirpath)
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

def makeparentdir(absPath):
    parentPath = os.path.dirname(absPath)
    if os.path.isfile(parentPath) or os.path.isdir(parentPath):
        return True
    else:
        if makeparentdir(parentPath) == True:
            os.mkdir(parentPath)
    return True