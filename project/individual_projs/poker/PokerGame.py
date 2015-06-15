# -*- coding: utf-8 -*-
import sys
from PokerCard import PokerCardPool

reload(sys)
sys.setdefaultencoding('utf-8')

class PokerGame(object):

    def __init__(self, cardsetnum, removejoker):
        self.playerlist = []
        self.counter = 0
        self.forceend = False
        self.cardpool = PokerCardPool(cardsetnum, removejoker)

    def dealCard(self, playernum, cardnum):
        assert playernum >= 0
        assert playernum < len(self.playerlist)
        if cardnum > self.cardpool.getPoolSize():
            print "pool empty"
            self.forceend = True
        else:
            deallist = self.cardpool.dealCardsFromPool(cardnum)
            self.playerlist[playernum].cardlist.extend(deallist)

    def gameLoop(self):
        while self.checkGameEnd() == False:
            print "\n\nrun in game"
            self.runOneLoopGame()
            self.balanceResult()

    def resetPlayerStatus(self):
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'resetStatus'):
                eachplayer.resetStatus()

    def runOneLoopGame(self):
        assert len(self.playerlist) > 0
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'playGame'):
                eachplayer.playGame()
        self.dealInGamePlayerCard()

    def dealInGamePlayerCard(self):
        pass

    def checkGameEnd(self):
        assert len(self.playerlist) > 0
        if self.forceend == True:
            return True
        playercounter = 0
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'ingame'):
                if eachplayer.ingame == True:
                    playercounter += 1
        if playercounter > 1:
            return False
        return True

    def balanceResult(self):
        pass

    def getStatusInfo(self):
        statusinfo = "==== curr game status ====\n"
        statusinfo += "game count: %d\t" % (self.counter)
        statusinfo += "remain cards: %d\n" % (self.cardpool.getPoolSize())
        return statusinfo
