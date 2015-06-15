# -*- coding: utf-8 -*-
import sys
from PokerPlayer import PokerPlayer
from PokerCard import PokerCard

reload(sys)
sys.setdefaultencoding('utf-8')

class BlackJackPlayer(PokerPlayer):
    Ready = 0
    Hit = 1
    Stand = 2
    Bust = 3

    def __init__(self, number, fund, isbanker):
        super(BlackJackPlayer, self).__init__(number, fund)
        self.isbanker = isbanker

    def getStatusInfo(self):
        infostr = super(BlackJackPlayer, self).getStatusInfo()
        infostr += "\n\tcurrent value: %d" % (self.calculateTotalValue())
        return infostr

    def calculateTotalValue(self):
        totalval = 0
        existace = False
        for eachcard in self.cardlist:
            singlevalue = PokerCard(eachcard).getCardValue() + 1
            if singlevalue == 1:
                existace = True
            elif singlevalue > 10:
                singlevalue = 10
            totalval += singlevalue
        if existace == True and totalval < 12:
            totalval += 10
        return totalval

    def isBlackJack(self):
        value = self.calculateTotalValue()
        if value == 21 and len(self.cardlist) == 2:
            return True
        return False

    def isBust(self):
        return self.status == self.Bust

    def decideNextOperate(self):
        value = self.calculateTotalValue()
        if value < 18:
            return self.Hit
        elif value < 22:
            return self.Stand
        return self.Bust

    def playGame(self):
        super(BlackJackPlayer, self).playGame()
        if self.status == self.Ready:
            self.currbet = 100
            self.status = self.Hit
        elif self.status == self.Hit:
            self.status = self.decideNextOperate()
        else:
            pass
        print "player %d choice: %d" % (self.playernumber, self.status)
        print "\tvalue: %d" % (self.calculateTotalValue())
