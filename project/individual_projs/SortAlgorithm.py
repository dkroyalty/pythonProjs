# -*- coding: utf-8 -*-
import sys
import os
import re
import random

sys.path.append("..")
from base_py._baseexecuteoperate import *

reload(sys)
sys.setdefaultencoding('utf-8')

def GenerateRandomList(length):
    randomlist = []
    rangemax = length*2
    for i in range(length):
        randomlist.append(random.randint(0, rangemax))
    return randomlist

def TestCase():
    originlist = GenerateRandomList(1000)
    testlist = [
        QuickSort,
        MergeSort,
        HeapSort,
        SelectionSort,
        BubbleSort,
        InsertSort,
        ShellSort,
    ]
    for eachfunc in testlist:
        rst = eachfunc(list(originlist))
        print "check %s" % eachfunc.__name__
        CheckListSortRst(list(originlist), rst)

def CheckListSortRst(srclist, checklist):
    srclist.sort()
    checkrst = True
    if not len(srclist) == len(checklist):
        print "ILLEGAL"
        return
    for i, eachitem in enumerate(srclist):
        if not eachitem == checklist[i]:
            checkrst = False
            break
    if checkrst == True:
        print "OK..."
    else:
        print "FAIL"
        print "expect: "
        print srclist
        print "current: "
        print checklist

def QuickSort(srclist, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(srclist)-1
    i = low
    j = high
    if i >= j:
        return srclist
    key = srclist[i]
    while i < j:
        while i < j and srclist[j] >= key:
            j = j-1
        srclist[i] = srclist[j]
        while i < j and srclist[i] <= key:
            i = i+1
        srclist[j] = srclist[i]
    srclist[i] = key
    QuickSort(srclist, low, i-1)
    QuickSort(srclist, j+1, high)
    return srclist

def MergeSort(srclist):
    if len(srclist) <=1:
        return srclist
    num = len(srclist)/2
    left = MergeSort(srclist[:num])
    right = MergeSort(srclist[num:])
    return Merge(left,right)

def Merge(left,right):
    r,l=0,0
    reslut=[]
    while l<len(left) and r<len(right):
        if left[l] < right[r]:
            reslut.append(left[l])
            l+=1
        else:
            reslut.append(right[r])
            r+=1
    reslut += right[r:]
    reslut += left[l:]
    return reslut

# a kind of selection sort
def HeapSort(srclist):
    for start in range((len(srclist)-2)/2, -1, -1):
        SiftDown(srclist, start, len(srclist)-1)
    for end in range(len(srclist)-1, 0, -1):
        # move first to end for list[0] is the largest for list[0:end]
        srclist[0],srclist[end] = srclist[end],srclist[0]
        SiftDown(srclist,0,end-1)
    return srclist

# adjust to build a large end binary heap [the first element is the largest]
# featrue: k[i] >= k[2*i] && k[i] >= k[2i+1]
def SiftDown(srclist, start, end):
    root = start
    while True:
        child = 2*root+1
        if child>end:
            break
        if child+1<=end and srclist[child]<srclist[child+1]:
            child += 1
        if srclist[root]<srclist[child]:
            srclist[root],srclist[child] = srclist[child],srclist[root]
            root = child
        else:
            break

# the basic selection sort
def SelectionSort(srclist):
    for i in range(0, len (srclist)):
        minimum = i
        for j in range(i + 1, len(srclist)):
            if srclist[j] < srclist[minimum]:
                minimum = j
        srclist[i], srclist[minimum] = srclist[minimum], srclist[i]
    return srclist

def BubbleSort(srclist):
    length = len(srclist)
    while length > 0:
        for i in range(length - 1):
            if srclist[i] > srclist[i+1]:
                srclist[i], srclist[i+1] = srclist[i+1], srclist[i]
        length -= 1
    return srclist

def InsertSort(srclist):
    length = 1
    while length < len(srclist):
        for i in range(length):
            if srclist[length] < srclist[i]:
                val = srclist[length:length+1]
                for j in range(length, i, -1):
                    srclist[j] = srclist[j-1]
                srclist[i] = val[0]
                break
        length += 1
    return srclist

def ShellSort(srclist):
    length = len(srclist)
    step = GetDeltaStep(length)
    while step >= 1:
        for i in range(step,length):
            j = i
            while j>=step and srclist[j]<srclist[j-step]:
                srclist[j],srclist[j-step] = srclist[j-step],srclist[j]
                j -= step
        if step == 1:
            break
        step = GetDeltaStep(length, step)
    return srclist

def GetDeltaStep(length, prev=None):
    step = 1
    divval = 2
    #sample
    if False:
        if prev is None:
            while step < length//3:
                step = 3*step+1
        else:
            step = prev // 3
    #Shell delta
    if False:
        if prev is None:
            step = length // divval
        else:
            step = prev // divval
    #Hibbard delta
    if True:
        if prev is None:
            step = length // divval - 1
        else:
            step = prev // divval - 1
    if step < 1:
        step = 1
    return step

if __name__ == "__main__":
    TestCase()
