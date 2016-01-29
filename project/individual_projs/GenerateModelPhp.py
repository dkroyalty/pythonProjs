#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import os.path
import sys
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

modelPath = '/Users/kangzan/Project/shironeko/shironeko-gna/gna_php/application/models'
operateDict = dict()

def LoadParamArguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--source', dest='source', 
        #choices=[''],
        required=True)
    argparser.add_argument('-o', '--output',  dest='output',
        default=None, const=OutputFile, nargs='?')
    args = argparser.parse_args()
    paramdict = dict()
    paramdict['source'] = getattr(args, 'source', None)
    paramdict['function'] = []
    paramdict['function'].append(getattr(args, 'output', None))
    return paramdict

def LoadSqlTableDict(sqlContent):
    tableData = re.findall(r'CREATE TABLE[\w\W]*?;', sqlContent)
    tableDict = dict()
    for each in tableData:
        tableName, colList = BuildTableInfo(each)
        tableDict[tableName] = colList
    return tableDict

def BuildTableInfo(createSql):
    tableName = re.search(r'CREATE TABLE `(.*?)`', createSql).group(1)
    colList = re.findall(r'\n +`(.*?)` (\w*?)[ \(]', createSql)
    return tableName, colList

def OutputFile():
    for eachTable in operateDict.keys():
        OutputToMapper(eachTable)
        OutputToModel(eachTable, operateDict[eachTable])

def OutputToModel(tableName, colList):
    modelName = ConvertModelName(tableName)
    fileName = "Model%s.php" % (modelName)
    outputFile = os.path.join(modelPath, fileName)
    declareCol = GenerateDeclare(colList)
    setColType = GenerateColType(colList)
    getFuncStr = GenerateGetFunc(colList)
    setFuncStr = GenerateSetFunc(colList)
    content = "<?php\n\n\
class Application_Model_%s extends Application_Model_ModelAbstract\n{\n\n\
%s\
\tprotected static $dataTypes = array(\n%s\
\t\t);\n\n\
\tpublic function __construct($data = null, $create = true)\n\
\t{\n\
\t\tparent::_init(self::$dataTypes, $data, $create);\n\
\t}\n\n\
%s%s\
}\n\n" % (modelName, declareCol, setColType, getFuncStr, setFuncStr)
    with open(outputFile, 'wb') as fileWriter:
        fileWriter.write(content)

def GetDefaultValByType(paramType):
    paramDefaultDict = {
        'int': '0',
        'varchar': '\'\'',
    }
    if paramType in paramDefaultDict.keys():
        return paramDefaultDict[paramType]
    return 'null'

def GenerateDeclare(colList):
    declareStr = ""
    for each in colList:
        declareStr += "\tprotected $_%s = %s;\n\n" % (each[0], GetDefaultValByType(each[1]))
    return declareStr

def GenerateColType(colList):
    colStr = ""
    convertDict = {
        'int': 'int',
        'date': 'Date',
    }
    for each in colList:
        if each[1] in convertDict.keys():
            colStr += "\t\t'%s' => '%s',\n" % (each[0], convertDict[each[1]])
    return colStr

def GenerateGetFunc(colList):
    getFuncStr = ""
    for each in colList:
        getFuncStr += "\tpublic function get%s() {\n\t\treturn $this->_%s;\n\t}\n\n" % \
            (re.sub(r'^(\w)', lambda f: f.group(1).upper(), each[0]), each[0])
    return getFuncStr

def GenerateSetFunc(colList):
    setFuncStr = ""
    for each in colList:
        setFuncStr += "\tpublic function set%s($%s) {\n\t\t$this->_%s = $%s;\n\t\t$this->_updatedColumns['%s'] = 1;\n\t}\n\n" % \
            (re.sub(r'^(\w)', lambda f: f.group(1).upper(), each[0]), each[0], each[0], each[0], each[0])
    return setFuncStr

def OutputToMapper(tableName):
    modelName = ConvertModelName(tableName)
    fileName = "mappers/Mapper%s.php" % (modelName)
    outputFile = os.path.join(modelPath, fileName)
    content = "<?php\n\n\
class Application_Model_Mapper_%s extends Application_Model_Mapper_MapperAbstract\n{\n\n\
\tprotected $_rowClass = 'Application_Model_%s';\n\n\
\tprotected $_tableName = '%s';\n\n\
\tprotected $_hasCreatedAt = true;\n\n\
\tprotected $_hasUpdatedAt = true;\n\n\
}\n\n" % (modelName, modelName, tableName)
    with open(outputFile, 'wb') as fileWriter:
        fileWriter.write(content)

def ConvertModelName(tableName):
    modelName = re.sub(r'^(\w)', lambda f: f.group(1).upper(), tableName)
    modelName = re.sub(r'(\_)(\w)', lambda f: f.group(2).upper(), modelName)
    return modelName

if __name__ == "__main__":
    paramdict = LoadParamArguments()
    print "now path: %s" % (os.getcwd())
    print paramdict
    if not os.path.isfile(paramdict['source']):
        print 'not exist source file'
        exit(0)
    with open(paramdict['source'], 'rb') as fileHandler:
        content = fileHandler.read()
    operateDict = LoadSqlTableDict(content)
    for eachfunc in paramdict['function']:
        if eachfunc is not None:
            if hasattr(eachfunc, '__call__'):
                print eachfunc.__name__
                eachfunc.__call__()
