# -*- coding: utf-8 -*-
import sys
import os
import os.path as path
import struct
import re
import zlib
import argparse

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

import binascii

def GenBytesData(info):
    bytes = None
    if isinstance(info, str):
        pattern = '%dc' % (len(info))
        bytes = struct.pack(pattern, *info)
    elif isinstance(info, int):
        # format
        # > big-endian: eg  13 -> 0x0000000d
        # < little-endian: eg  13 -> 0x0d000000
        bytes = struct.pack('>i', info)
    assert bytes is not None
    return bytes

def GenCrc32BytesData(strval):
    data = (binascii.crc32(strval) & 0xffffffff)
    bytes = struct.pack('>I', data)
    return bytes

def ConvertByteData(byteformat, data, contuple):
    datasize = len(data)
    dataformat = '%d%s' % (datasize, byteformat)
    convertdata = None
    if contuple == True:
        convertdata = struct.unpack(dataformat, data)
    else:
        assert isinstance(data, tuple)
        convertdata = struct.pack(dataformat, *data)
    return convertdata


class PngIdatStruct(object):

    def __init__(self, rawdata, detaildict):
        self.rawdata = rawdata
        self.detaildict = detaildict
        self.linedatalist = []
        self.filterlist = ['None', 'Sub', 'Up', 'Average', 'Paeth']
        print detaildict
        self.BuildPixelInfo()
        self.ConvertNoneFilter()
        print self.linedatalist[0]

    def DecompressData(self, rawdata):
        decompobj = zlib.decompressobj()
        decompdata = decompobj.decompress(rawdata)
        decompdata += decompobj.flush()
        tupledata = ConvertByteData('B', decompdata, True)
        return tupledata

    # weird that the compressed data cannot be the rawdata...
    def CompressData(self, tupledata, complevel):
        bytedata = ConvertByteData('B', tupledata, False)
        compobj = zlib.compressobj(complevel)
        compdata = compobj.compress(bytedata)
        compdata += compobj.flush()
        return compdata

    def BuildPixelInfo(self):
        tupledata = self.DecompressData(self.rawdata)
        linetotal = int(len(tupledata) / self.detaildict['height'])
        assert linetotal*self.detaildict['height'] == len(tupledata)
        pixelbits = int((linetotal-1) / self.detaildict['width'])
        assert pixelbits*self.detaildict['width'] == (linetotal-1)
        for hcnt in range(0, self.detaildict['height']):
            linedatadict = dict()
            linepos = hcnt*linetotal
            filtertype = tupledata[linepos]
            linepos += 1
            linedatadict['filter'] = self.filterlist[filtertype]
            linedatadict['data'] = []
            print 'filter type: %s' % (self.filterlist[filtertype])
            for wcnt in range(0, self.detaildict['width']):
                datalist = tupledata[linepos: linepos+pixelbits]
                linedatadict['data'].append(datalist)
                linepos += pixelbits
                print datalist
            self.linedatalist.append(linedatadict)

    def ConvertNoneFilter(self):
        for eachlinedata in self.linedatalist:
            filtername = eachlinedata['filter']
            exestr = "self.FilterBack%s(eachlinedata['data'])" % (filtername)
            eachlinedata['data'] = eval(exestr)

    def FilterBackNone(self, rawdata):
        return rawdata

    def FilterBackSub(self, rawdata):
        for i in range(1, len(rawdata)):
            for j in range(0, len(rawdata[i])):
                rawdata[i][j] = rawdata[i-1][j] + rawdata[i][j]

    def FilterBackUp(self, rawdata):
        return rawdata

    def FilterBackAverage(self, rawdata):
        return rawdata

    def FilterBackPaeth(self, rawdata):
        return rawdata


class PngStruct(object):

    def __init__(self, filepath, outputsuffix):
        self.file = filepath
        self.outfile = filepath
        if outputsuffix is not None:
            self.outfile += outputsuffix
        self.commonstart = '\x89PNG\x0D\x0A\x1A\x0A'
        self.chunkorderlist = []
        self.chunkdict = dict()
        self.datlist = []
        self.detaildict = dict()
        self.idatdata = None
        self.criticalchunk = set(['IHDR', 'IDAT', 'IEND'])
        self.BuildChunkDicts()
        self.GatherPngDetail()

    def BuildChunkDicts(self):
        startpos = len(GenBytesData(self.commonstart))
        curpos = 0
        f = open(self.file, 'rb')
        f.seek(startpos, 0)
        while True:
            try:
                subchunkdict = dict()
                size = struct.unpack('>i', f.read(4))[0]
                name = ''.join(struct.unpack('4c', f.read(4)))
                content = f.read(size)
                crc = f.read(4)
                subchunkdict['name'] = name
                subchunkdict['size'] = size
                subchunkdict['content'] = content
                subchunkdict['crc'] = crc
                self.chunkorderlist.append(name)
                self.chunkdict[name] = subchunkdict
                curpos = f.tell()
            except:
                break
        f.close()

    def GatherPngDetail(self):
        assert len(self.chunkorderlist) > 0
        assert len(self.chunkdict) > 0
        if 'IHDR' in self.chunkorderlist:
            chunkdict = self.chunkdict['IHDR']
            self.GatherIHDRDetailData(chunkdict['content'])
        if False and 'IDAT' in self.chunkorderlist:
            chunkdict = self.chunkdict['IDAT']
            self.idatdata = PngIdatStruct(chunkdict['content'], self.detaildict)
        print self.detaildict

    def LogPngStatus(self):
        for chunkname in self.chunkorderlist:
            print "---- %s ----" % (chunkname)
            chunkdict = self.chunkdict[chunkname]
            print "size : %d" % (chunkdict['size'])
            #print "crc : %s" % (chunkdict['crc'])
            crc = '0x'
            for item in struct.unpack('4B', chunkdict['crc']):
                crc += re.sub('^0x', '', hex(item))
            print "crc : %s" % (crc)
            if self.CheckChunkCrc(chunkdict) == True:
                print "CRC check pass"
            else:
                print "CRC check fail"

    def CheckChunkCrc(self, chunkdict):
        assert isinstance(chunkdict, dict)
        checkdata = GenBytesData(chunkdict['name'])
        checkdata += chunkdict['content']
        gencrc = GenCrc32BytesData(checkdata)
        #print struct.unpack('4B', chunkdict['crc'])
        #print struct.unpack('4B', gencrc)
        return gencrc == chunkdict['crc']

    def GatherIHDRDetailData(self, bytedata):
        detail = struct.unpack('>IIBBBBB', bytedata)
        self.detaildict['width'] = detail[0]
        self.detaildict['height'] = detail[1]
        # bitdepth stands for the image depth:
        # index map image [1, 2, 4, 8] 
        # gray image [1, 2, 4, 8, 16] 
        # true color image [8, 16] 
        self.detaildict['bitdepth'] = detail[2]
        # colortype decides image type:
        # 0 - gray [no alpha]
        # 2 - true color [no alpha]
        # 3 - index map
        # 4 - gray [with alpha]
        # 6 - true color [with alpha]
        self.detaildict['compresstype'] = detail[3]
        self.detaildict['colortype'] = detail[4]
        self.detaildict['filtertype'] = detail[5]
        self.detaildict['interlace'] = detail[6]

    def GenerateChunkBytesData(self, chunkdict):
        assert isinstance(chunkdict, dict)
        bytedata = ''
        bytedata += GenBytesData(chunkdict['size'])
        bytedata += GenBytesData(chunkdict['name'])
        bytedata += chunkdict['content']
        bytedata += chunkdict['crc']
        return bytedata

    def ExportWithGivenChunk(self, chunkset):
        assert isinstance(chunkset, set)
        assert self.criticalchunk.issubset(chunkset)
        f = open(self.outfile, 'wb')
        f.write(GenBytesData(self.commonstart))
        for chunkname in self.chunkorderlist:
            if chunkname in chunkset:
                f.write(self.GenerateChunkBytesData(self.chunkdict[chunkname]))
        f.close()

def LoadParamArguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--file',
        dest='opefile', help='operate filename')
    argparser.add_argument('-d', '--dir',
        dest='opedir', help='operate dir')
    argparser.add_argument('-i', '--info',
        dest='infomation', help='output detail info')
    argparser.add_argument('-o', '--output',
        dest='outputsuffix', help='output filename')
    args = argparser.parse_args()
    paramdict = dict()
    paramdict['opefile'] = getattr(args, 'opefile', None)
    paramdict['opedir'] = getattr(args, 'opedir', None)
    paramdict['infomation'] = getattr(args, 'infomation', None)
    paramdict['outputsuffix'] = getattr(args, 'outputsuffix', None)
    return paramdict

def CompressPngLocal():
    paramdict = LoadParamArguments()
    print paramdict
    pnglist = []
    if paramdict['opedir'] and path.isdir(paramdict['opedir']):
        operatedir = paramdict['opedir']
        pnglist = getSearchedFilesInDirWithAbsPath(operatedir, [r'\.png$'])
    elif paramdict['opefile'] and path.isfile(paramdict['opefile']):
        if re.search(r'\.png$', paramdict['opefile'].lower()):
            pnglist.append(paramdict['opefile'])
    for each in pnglist:
        struct = PngStruct(each, paramdict['outputsuffix'])
        if paramdict['infomation']:
            struct.LogPngStatus()
        struct.ExportWithGivenChunk(set(['IHDR', 'IDAT', 'IEND']))

if __name__ == "__main__":
    try:
        CompressPngLocal()
    except:
        print >> sys.stderr, u'fail to operate'
        raise
