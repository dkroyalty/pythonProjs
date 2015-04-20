# -*- coding: utf-8 -*-
import sys
import os
import re
import itertools

reload(sys)
sys.setdefaultencoding('utf-8')

#Comment:calculate 24 from 4 numbers
#Param:1
OPERATE_DICT = {
    0: "+",
    1: "-",
    2: "*",
    3: "/",
}
CALC_ODRDER_LIST = [
    " {0}.0 {1} {2}.0 {3} {4}.0 {5} {6}.0",
    "({0}.0 {1} {2}.0){3} {4}.0 {5} {6}.0",
    " {0}.0 {1}({2}.0 {3} {4}.0){5} {6}.0",
    " {0}.0 {1} {2}.0 {3}({4}.0 {5} {6}.0)",
    "({0}.0 {1} {2}.0 {3} {4}.0){5} {6}.0",
    " {0}.0 {1}({2}.0 {3} {4}.0 {5} {6}.0)",
    "({0}.0 {1} {2}.0){3}({4}.0 {5} {6}.0)",
]

def GetNumberListFromParam(param):
    paramList = param.strip().split(' ')
    retList = []
    for each in paramList:
        if str(int(each)) == str(each):
            retList.append(int(each))
    retList.sort()
    if len(retList) < 1:
        print "not legal input value: %s" % param
        exit(-1)
    return retList

# source code from itertool function product(iterable, repeattime)
def GetFullNumSequence(*args, **kwds):
     pools = map(tuple, args) * kwds.get('repeat', 1)
     result = [[]]
     for pool in pools:
         result = [x+[y] for x in result for y in pool]
     for prod in result:
         yield tuple(prod)

# source code from itertool function permutations(iterable [,r])
def GetAllPossibleNumSequence(inputList, r=None):
    # it is a intresting function which I cannot understand at a glance
    # the basic method is output through the index list indices
    # just skip the origin input data, because it's not important
    # for example: the permutations of the list [0 1 2]
    # (0, 1, 2)
    # (0, 2, 1)
    # (1, 0, 2)
    # (1, 2, 0)
    # (2, 0, 1)
    # (2, 1, 0)
    pool = tuple(inputList)
    poolSize = len(pool)
    r = poolSize if r is None else r
    if r > poolSize:
        return
    indices = range(poolSize)
    # the most attractive array stands for the math
    # permutation size is the multiple of all elements in cycles
    cycles = range(poolSize, poolSize-r, -1)
    # first return value always be the input iterable
    yield tuple(pool[i] for i in indices[:r])
    detail = False
    while poolSize:
        # realize the count down for cycles to reduce the first element to zero
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                # keep the first element in indicies when change the followed
                # keep the followed element in order of value
                # do left loop shift for the indecies element start from i
                # for example:
                # i is 2 : [0 1 2 3] -> [0 1 3 2]
                # i is 1 : [0 1 2 3] -> [0 2 3 1]
                indices[i:] = indices[i+1:] + indices[i:i+1]
                # reset number in check list cycle when it comes to zero
                cycles[i] = poolSize - i
            else:
                j = cycles[i]
                # exchange position according to cycle list
                # here is an exactly loop sequence to ensure the result
                # for example: [0 1 2 3]: i j pair will become [j count reverse]
                # 2 1 -> 1 2 -> 2 1 -> 1 1 -> 2 1 -> 0 3
                # 2 1 -> 1 2 -> 2 1 -> 1 1 -> 2 1 -> 0 2
                # 2 1 -> 1 2 -> 2 1 -> 1 1 -> 2 1 -> 0 1
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            # only execute when the for loop end without break
            # the cycles list will be reset to the origin state
            return

def GetAllPossibleNumberOrder(numberList):
    possibleList = []
    for item in list(GetAllPossibleNumSequence(numberList)):
        if item not in possibleList:
            possibleList.append(item)
    return possibleList

def GetAllPossibleCalculatOrder(totalCalcTime):
    operateList = []
    for item in list(GetFullNumSequence(OPERATE_DICT, repeat=totalCalcTime)):
        if item not in operateList:
            operateList.append(item)
    return operateList

def DoTwentyFourCalculate(param):
    numberList = GetNumberListFromParam(param)
    possibleList = GetAllPossibleNumberOrder(numberList)
    operateList = GetAllPossibleCalculatOrder(len(numberList)-1)
    resultList = []
    for eachseq in possibleList:
        for eachCalc in operateList:
            for eachComb in CALC_ODRDER_LIST:
                calcEquation = CalcCombination(eachseq, eachCalc, eachComb)
                if CheckCalculateResult(calcEquation) == True:
                    resultList.append(calcEquation)
                    print calcEquation
    print resultList

def CheckCalculateResult(strEquation):
    rst = 0.0
    try:
        rst = eval(strEquation)
    except:
        pass
    if rst == 24.0 and (rst-int(rst)) < 0.00001:
        return True
    return False

def CalcCombination(iterNum, iterOpe, calcPattern):
    basicList = TakeOperateInEquation(iterNum, iterOpe)
    strEquation = calcPattern.format(*basicList)
    return strEquation

def TakeOperateInEquation(iterNum, iterOpe):
    equationList = []
    numList = list(iterNum)
    opeList = list(iterOpe)
    while len(numList)>0 or len(opeList)>0:
        if len(numList) > 0:
            equationList.append(numList.pop(0))
        if len(opeList) > 0:
            equationList.append(OPERATE_DICT[opeList.pop(0)])
    return equationList

if __name__ == "__main__":
    param = ""
    if len(sys.argv) > 1:
        param = sys.argv[1]
    if len(param) == 0:
        print "not legal input parameter"
    else:
        DoTwentyFourCalculate(param)
