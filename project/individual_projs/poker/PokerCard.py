# -*- coding: utf-8 -*-
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

class PokerCardPool(object):

    def __init__(self, duplicatetimes=1, isspecial=False):
        assert duplicatetimes > 0
        self.cardpool = []
        for i in range(duplicatetimes):
            if isspecial == False:
                self.cardpool.append(1000000)
                self.cardpool.append(1000001)
            for color in range(2, 6):
                for pt in range(len(PokerCard._CardPointList)):
                    self.cardpool.append(10**color+pt)

    def dealCardsFromPool(self, times=1):
        deallist = []
        i = 0
        while i < times:
            selcard = random.randint(0, len(self.cardpool)-1)
            deallist.append(self.cardpool[selcard])
            self.cardpool.remove(self.cardpool[selcard])
            i += 1
        return deallist

    def getPoolSize(self):
        return len(self.cardpool)

    def displayPoolInfo(self):
        for eachcard in self.cardpool:
            print PokerCard(eachcard).getCardInfo()

class PokerCard(object):

    _CardBiasDict = {
        "Diamond":100,
        "Club":   1000,
        "Heart":  10000,
        "Spade":  100000,
        "Joker":  1000000,
    }
    _CardPointList = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, cardvalue):
        assert self.checkValueLegal(cardvalue)
        self.cardvalue = cardvalue
        self.status = 0

    def checkIsJoker(self, value):
        val = value - self._CardBiasDict["Joker"]
        if val == 0 or val == 1:
            return True
        return False

    def checkValueLegal(self, cardvalue):
        cardtype = self.getGivenCardType(cardvalue)
        assert cardtype is not None
        val = self.getGivenCardValue(cardvalue)
        if self.checkIsJoker(cardvalue):
            return True
        elif val not in range(len(self._CardPointList)):
            return False
        return True

    def getCardType(self):
        return self.getGivenCardType(self.cardvalue)

    def getCardValue(self):
        return self.getGivenCardValue(self.cardvalue)

    def getGivenCardValue(self, value):
        for eachkey in self._CardBiasDict.keys():
            delta = value - self._CardBiasDict[eachkey]
            if delta >= 0 and delta < 20:
                return value % self._CardBiasDict[eachkey]
        return None

    def getGivenCardType(self, value):
        for eachkey in self._CardBiasDict.keys():
            delta = value - self._CardBiasDict[eachkey]
            if delta >= 0 and delta < 20:
                return eachkey
        return None

    def getCardInfo(self):
        infostr = ""
        fullname = self.getGivenCardType(self.cardvalue)
        if self.checkIsJoker(self.cardvalue):
            infostr = "%s-%d" % (fullname, self.getGivenCardValue(self.cardvalue))
        else:
            infostr = "%s-%s" % (fullname,
                self._CardPointList[self.getGivenCardValue(self.cardvalue)])
        return infostr

if __name__ == "__main__":
    testpool = PokerCardPool()
    #print testpool.dealCardsFromPool(5)
    testpool.displayPoolInfo()
