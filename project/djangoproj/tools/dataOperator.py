# -*- coding: utf-8 -*-
import sys
import os
import re
from os import path
import datetime
import cStringIO as StringIO
import argparse

from xlrd import open_workbook, xldate_as_tuple, cellname, cellnameabs
import simplejson as json
import yaml

reload(sys)
sys.setdefaultencoding('utf-8')

def to_colx(colname):
    a2z = 'ABCDEFGHIJLKMNOPQRSTUVWXYZ'
    total = 0
    mult = 0
    for char in colname:
        total += (a2z.find(char) + (26 * mult))
    mult += 1
    return total

class SettingColumn(object):

    def __init__(self, yaml, column):
        self.yaml = yaml
        self.column = column
        self.name = column['name']
        self.type = column['type']
        self.default = column['default'] if 'default' in column else None

class SettingsYaml(object):

    def __init__(self, yamldict, setpath=None):
        self.yaml = yamldict
        self.path = setpath
        self.model = yamldict['table']['model']
        columns = yamldict['table']['columns']
        self.columns = dict()
        for column in columns:
            self.columns[column['column']] = column

    def createSettingColumn(self, column):
        return SettingColumn(self, column)

    def isConvertSheet(self, sheet):
        if self.yaml['table']['sheet'] == sheet.name:
            return True
        return False

    def createSettingColumn(self, column):
        if self.columns.has_key(column):
            return SettingColumn(self, self.columns[column])
        return None

    def getConvertSheetName(self):
        return self.yaml['table']['sheet']

    def convertSheet(self, sheet):
        if self.isConvertSheet(sheet):
            s = sheet
            self.row = self.yaml['table']['row'] - 1 
            self.settingcolumns = dict()
            self.columninfo = dict()
            yamlcolset = set(self.columns)
            xlscolset = set()
            for col in range(s.ncols):
                column = s.cell(self.row, col).value
                self.columninfo[column] = col
                if column in self.columns:
                    xlscolset.add(column)
                    self.settingcolumns[col] = self.createSettingColumn(column)

            outyamlcolumns = list(yamlcolset - xlscolset)
            self.outyamlsettingcolumns = []
            for outyamlcolumn in outyamlcolumns:
                if self.columns[outyamlcolumn].has_key('default'):
                    default = self.columns[outyamlcolumn]['default']
                    self.outyamlsettingcolumns.append(self.createSettingColumn(outyamlcolumn))
            self.outyamlcolumns = outyamlcolumns

    def getSettingColumn(self, row, column):
        if row <= self.row:
            return None
        if column in self.settingcolumns:
            return self.settingcolumns[column]
        return None

def xls2fix(s, settings, outputfile):
    fixture_list = []
    check_list = {}
    duplicatelist = {}
    rank_group_count = {}
    id = 0
    for row in range(s.nrows):
        rows = []
        for col in range(s.ncols):
            rows.append(s.cell(row, col).value)
        if row <= settings.row:
            continue
        fields = {}
        id += 1
        for column, col in enumerate(rows):
            settingcolumn = settings.getSettingColumn(row, column)
            if settingcolumn:
                value = col
                # datetime
                if settingcolumn.type == 'datetime':
                    try:
                        timeVal = datetime.datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        timeVal = datetime.datetime.now()
                    value = timeVal.strftime("%Y-%m-%d %H:%M:%S")
                # date
                elif settingcolumn.type == 'date':
                    try:
                        timeVal = datetime.datetime.strptime(str(value), "%Y-%m-%d")
                    except ValueError:
                        timeVal = datetime.date.today()
                    value = timeVal.strftime("%Y-%m-%d")
                # time
                elif settingcolumn.type == 'time':
                    if value != '':
                        tmp = xldate_as_tuple(value, 0)
                        value = str(datetime.time(tmp[3], tmp[4], tmp[5]))
                    else:
                        value = None
                # char
                elif settingcolumn.type == 'char':
                    if isinstance(value, int):
                        value = '%d' % (value)
                    if isinstance(value, float):
                        value = '%f' % (value)
                    value = re.sub(r'\.0*$', '', value)
                    if settingcolumn.column.has_key('default'):
                        if value == '':
                            value = settingcolumn.column['default']
                            if value == 'None':
                                value = None
                    if settingcolumn.column.has_key('try_int'):
                        try:
                            if value == int(value):
                                value = int(value)
                        except:
                            pass
                # int
                elif settingcolumn.type == 'int':
                    try:
                        if value == u'':
                            value = 0
                            if settingcolumn.column.has_key('default'):
                                value = settingcolumn.column['default']
                                if value == 'None':
                                    value = None
                        else:
                            value = int(value)
                    except ValueError, UnicodeEncodeError:
                        print settingcolumn.name, value
                # float
                elif settingcolumn.type == 'float':
                    try:
                        value = float(col)
                    except ValueError:
                        value = 0.0
                # boolean
                elif settingcolumn.type == 'boolean':
                    if col == 'None':
                        value = None
                    elif len(unicode(col)) == 0:
                        value = False
                    else:
                        value = True
                # bit_field
                elif settingcolumn.type == 'bit_field':
                    extend_info = settingcolumn.column['extend']
                    value = 0

                    for i, extend in enumerate(extend_info):
                        idx = settings.columninfo[extend['column']] 
                        v = int(bool(rows[idx]))
                        value |= (v << i)
                # error
                else:
                    print u'unavailable data type %s' % (settingcolumn.type)
                    raise Exception()
                # id duplicate check
                if settingcolumn.name == 'id':
                    id = int(value)
                    duplicationCheck(id, check_list, duplicatelist)
                else:
                    fields[settingcolumn.name] = value
        # fields for columns not in yaml
        for settingcolumn in settings.outyamlsettingcolumns:
            fields[settingcolumn.name] = str(settingcolumn.default)

        fixture_list.append({
                'model': settings.model,
                'pk': id,
                'fields': fields,
                })
    # output duplicate id info
    if duplicatelist:
        for id, num in duplicatelist.iteritems():
            print "dup [ID] :", id, " [count] :", num
        return
    # output to destination file
    fp = open(outputfile, 'w')
    fp.write(json.dumps(fixture_list, encoding='utf-8', indent=4*' ', ensure_ascii=False, sort_keys=True).encode('utf-8'))
    fp.close()

def duplicationCheck(checkid, check_list, duplicatelist):
    if check_list.has_key(checkid):
        check_list[checkid] += 1
        duplicatelist[checkid] = check_list[checkid]
        return
    check_list[checkid] = 0

def checkExistence(filepath):
    if isinstance(filepath, str):
        if os.path.isfile(filepath):
            return True
    print "%s is not a file" % (filepath)

def loadArguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--input',
        dest='inputfile', help='input filename')
    argparser.add_argument('-c', '--config',
        dest='configfile', help='yaml2json mapping confing filename')
    argparser.add_argument('-y', '--yaml',
        dest='yamlfile', help='yaml filename')
    argparser.add_argument('-o', '--output',
        dest='outputfile', help='output filename')
    args = argparser.parse_args()
    paramdict = dict()
    paramdict['inputfile'] = getattr(args, 'inputfile', None)
    paramdict['configfile'] = getattr(args, 'configfile', None)
    paramdict['yamlfile'] = getattr(args, 'yamlfile', None)
    paramdict['outputfile'] = getattr(args, 'outputfile', None)
    assert checkExistence(paramdict['inputfile'])
    return paramdict

def loadMappingList(paramdict):
    existconfig = checkExistence(paramdict['configfile'])
    existyaml = checkExistence(paramdict['yamlfile'])
    mappinglist = []
    if existconfig == True:
        with open(paramdict['configfile']) as handler:
            mapping = yaml.load(handler.read())
        yamlpath = os.path.join(os.getcwd(), mapping['relative_path']['yaml'])
        jsonpath = os.path.join(os.getcwd(), mapping['relative_path']['json'])
        for each in mapping['mapping']['setting']:
            settingdict = dict()
            settingdict['yamlfile'] = os.path.join(yamlpath, each['yaml'])
            settingdict['output'] = os.path.join(jsonpath, each['json'])
            mappinglist.append(settingdict)
    elif existyaml == True and isinstance(paramdict['outputfile'], str) == True:
        mappinglist = [{'yamlfile':paramdict['yamlfile'],
                        'output':paramdict['outputfile'],},]
    return mappinglist

def mainFunc():
    paramdict = loadArguments()
    mappinglist = loadMappingList(paramdict)

    print "Opening workbook %s" % paramdict['inputfile']
    logfile = StringIO.StringIO()
    wb = open_workbook(paramdict['inputfile'], logfile=logfile)
    print mappinglist
    for conf in mappinglist:
        settings = None
        yamlfile = conf['yamlfile']
        outputfile = conf['output']
        with open(yamlfile) as handler:
            setpath = path.dirname(path.abspath(yamlfile)) + u'/'
            settings = SettingsYaml(yaml.load(handler.read()), setpath=setpath)
        misssheet = True
        for s in wb.sheets():
            if settings.isConvertSheet(s):
                print u'\tSheet:%s -> %s' % (s.name, outputfile)
                settings.convertSheet(s)
                misssheet = False
                xls2fix(s, settings, outputfile)
        if misssheet == True:
            print u'*********************** %s [%s] ***********************' %\
                ('miss sheet', settings.getConvertSheetName())
            print u'*********************** %s [%s] ***********************' %\
                ('check yaml', yamlfile)
    print "excute end"

if __name__ == '__main__':
    try:
        mainFunc()
    except:
        print >> sys.stderr, u'fail to operate'
        raise
