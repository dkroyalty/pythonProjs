# -*- coding: utf-8 -*-
import sys
import os
import os.path as path
import struct
import re

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

class PngStruct(object):

    def __init__(self, filepath):
        self.file = filepath
        self.outfile = filepath + '.tmp'
        self.commonstart = '\x89PNG\x0D\x0A\x1A\x0A'
        self.chunklist = []
        self.criticalchunk = set(['IHDR', 'IDAT', 'IEND'])
        self.BuildChunkDicts()

    def BuildChunkDicts(self):
        startpos = len(GenBytesData(self.commonstart))
        curpos = 0
        f = open(self.file, 'rb')
        f.seek(startpos, 0)
        while True:
            try:
                chunkdict = dict()
                size = struct.unpack('>i', f.read(4))[0]
                name = ''.join(struct.unpack('4c', f.read(4)))
                content = f.read(size)
                crc = f.read(4)
                chunkdict['name'] = name
                chunkdict['size'] = size
                chunkdict['content'] = content
                chunkdict['crc'] = crc
                self.chunklist.append(chunkdict)
                curpos = f.tell()
            except:
                break
        f.close()

    def LogPngStatus(self):
        for eachchunk in self.chunklist:
            print "---- %s ----" % (eachchunk['name'])
            print "size : %d" % (eachchunk['size'])
            #print "crc : %s" % (eachchunk['crc'])
            crc = '0x'
            for item in struct.unpack('4B', eachchunk['crc']):
                crc += re.sub('^0x', '', hex(item))
            print "crc : %s" % (crc)
            if self.CheckChunkCrc(eachchunk) == True:
                print "CRC check pass"
        self.CheckPngDetail(eachchunk)

    def CheckChunkCrc(self, chunkdict):
        assert isinstance(chunkdict, dict)
        checkdata = GenBytesData(chunkdict['name'])
        checkdata += chunkdict['content']
        gencrc = GenCrc32BytesData(checkdata)
        #print struct.unpack('4B', chunkdict['crc'])
        #print struct.unpack('4B', gencrc)
        return gencrc == chunkdict['crc']

    def CheckPngDetail(self, chunkdict):
        assert isinstance(chunkdict, dict)
        for eachchunk in self.chunklist:
            if eachchunk['name'] == 'IHDR':
                detail = struct.unpack('>IIBBBBB', eachchunk['content'])
                print "width: %d" % (detail[0])
                print "height: %d" % (detail[1])
                print "bit depth: %d [%d]" % (detail[2], 2**detail[2])
                print "color: %d" % (detail[3])
                print "Interlace: %d" % (detail[-1])

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
        for eachchunk in self.chunklist:
            if eachchunk['name'] in chunkset:
                f.write(self.GenerateChunkBytesData(eachchunk))
        f.close()

def CompressPngLocal(inpath):
    pnglist = []
    if path.isdir(inpath):
        pnglist = getSearchedFilesInDirWithAbsPath(inpath, [r'\.png$'])
    elif path.isfile(inpath) and re.search(r'\.png$', inpath.lower()):
        pnglist.append(inpath)
    for each in pnglist:
        struct = PngStruct(each)
        struct.LogPngStatus()
        struct.ExportWithGivenChunk(set(['IHDR', 'IDAT', 'IEND']))

if __name__ == "__main__":
    param = ""
    if len(sys.argv) > 1:
        param = sys.argv[1]
    CompressPngLocal(param)
