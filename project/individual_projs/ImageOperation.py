# -*- coding: utf-8 -*-
import sys
import os
import re
from PIL import Image
from PIL import ImageChops

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

def CheckImageFile(imgfile):
    assert os.path.isfile(imgfile)
    im = Image.open(imgfile)
    print "image format: %s" % im.format
    print "image mode: %s" % im.mode
    print "image size: w={0},h={1}".format(*im.size)
    histolist = im.histogram()
    print "histoinfo len: %d | sum: %d" % (len(histolist), sum(histolist))
    splitim = im.split()
    for each in splitim:
        print "split histo sum: %d" % sum(each.histogram())

# the splitimglist order example:
#       0 1 2
#       3 4 5
#       6 7 8
def SplitOperateImage(imgfile, detaillv=1):
    assert os.path.isfile(imgfile)
    assert detaillv > 0
    im = Image.open(imgfile)
    assert detaillv < min(*im.size)
    splitimglist = []
    for y in range(detaillv):
        for x in range(detaillv):
            tmpx = int(x*im.size[0]/detaillv)
            tmpy = int(y*im.size[1]/detaillv)
            tmpw = int((x+1)*im.size[0]/detaillv)
            tmph = int((y+1)*im.size[1]/detaillv)
            bbox = (tmpx, tmpy, tmpw, tmph)
            splitimglist.append(im.crop(bbox))
    return splitimglist

def GenerateExtendImageFromSource(imgfile, splitlv=1, extendband=(5,5)):
    assert os.path.isfile(imgfile)
    assert splitlv > 0
    im = Image.open(imgfile)
    newsizex = im.size[0]+(splitlv-1)*extendband[0]
    newsizey = im.size[1]+(splitlv-1)*extendband[1]
    newim = Image.new("RGBA", (newsizex, newsizey), color="rgb(255,255,255)")
    splitimglist = SplitOperateImage(imgfile, splitlv)
    tmpy = 0
    for y in range(splitlv):
        tmpx = 0
        tmpy += (0 if y==0 else (splitimglist[splitlv*(y-1)].size[1] + extendband[1]))
        for x in range(splitlv):
            tmpx += (0 if x==0 else (splitimglist[splitlv*y+x-1].size[0] + extendband[0]))
            newim.paste(splitimglist[splitlv*y+x], (tmpx, tmpy))
    outname = "split_%s" % (os.path.basename(imgfile))
    outfile = os.path.join(os.path.dirname(imgfile), outname)
    newim.save(outfile, "PNG")

def GenerateSplitImageFromSource(imgfile, splitlv=1):
    assert os.path.isfile(imgfile)
    assert splitlv > 0
    splitimglist = SplitOperateImage(imgfile, splitlv)
    for i,each in enumerate(splitimglist):
        outname = "part%d_%s" % (i, os.path.basename(imgfile))
        outfile = os.path.join(os.path.dirname(imgfile), outname)
        each.save(outfile, "PNG")

def ComparaImageSimilarity(sourcefile, comparefile):
    assert os.path.isfile(sourcefile)
    assert os.path.isfile(comparefile)
    srcim = Image.open(sourcefile)
    cmpim = Image.open(comparefile)
    invim = ImageChops.invert(cmpim)
    checkim = Image.blend(srcim, invim, 0.5)
    #print checkim.histogram()
    rgbadict = GetImageRGBAInfoDict(srcim)
    rstdict = dict()
    for channelkey in rgbadict.keys():
        rstdict[channelkey] = GetStandardVarianceList(rgbadict[channelkey])
    print rstdict
    return rstdict

def GetImageRGBAInfoDict(img):
    assert img is not None
    rgbaim = img.convert('RGBA')
    imsize = rgbaim.size
    rgbadict = {'r':[], 'g':[], 'b':[], 'a':[]}
    for h in range(0, imsize[1]):
        for w in range(0, imsize[0]):
            pixelinfo = rgbaim.getpixel((w, h))
            assert len(pixelinfo) == 4
            rgbadict['r'].append(pixelinfo[0])
            rgbadict['g'].append(pixelinfo[1])
            rgbadict['b'].append(pixelinfo[2])
            rgbadict['a'].append(pixelinfo[3])
    return rgbadict

def GetStandardVarianceList(vallist):
    assert len(vallist) > 0
    averageval = sum(vallist)/len(vallist)
    varianceval = 0
    for i in vallist:
        varianceval += (i-averageval)**2
    stdvariance = (varianceval/len(vallist))**0.5
    return "%.2f" % stdvariance

if __name__ == "__main__":
    samplefile = 'sample'
    compfile = 'compare'
    CheckImageFile(samplefile)
    CheckImageFile(compfile)
    # split sample file into 9 parts, generate 9 files
    #GenerateSplitImageFromSource(samplefile, 3)
    # split sample file into 4 parts, put them into 1 file
    #GenerateExtendImageFromSource(samplefile, 2)
    # compare each pixel
    ComparaImageSimilarity(samplefile, compfile)
