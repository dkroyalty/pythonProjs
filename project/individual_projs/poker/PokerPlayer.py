# -*- coding: utf-8 -*-
import sys
from PokerCard import PokerCard

reload(sys)
sys.setdefaultencoding('utf-8')

class PokerPlayer(object):

    def __init__(self, number, fund):
        self.playernumber = number
        self.fundation = fund
        self.cardlist = []
        self.status = 0
        self.currbet = 0
        self.ingame = True
        self.dispcard = []

    def playGame(self):
        print ">>> player %d play game" % (self.playernumber)

    def quitGame(self):
        print ">>> player %d quit game" % (self.playernumber)
        self.ingame = False

    def resetStatus(self):
        for eachcard in self.dispcard:
            self.cardlist.remove(eachcard)
        self.dispcard = []
        self.currbet = 0

    def getStatusInfo(self):
        cardinfo = ""
        for eachcard in self.cardlist:
            cardinfo += "%s\t" % (PokerCard(eachcard).getCardInfo())
        infostr = "player: No %d, fund: %d, currbet: %d, cards: %s" % \
            (self.playernumber, self.fundation, self.currbet, cardinfo)
        return infostr