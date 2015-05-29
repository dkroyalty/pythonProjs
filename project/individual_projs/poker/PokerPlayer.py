# -*- coding: utf-8 -*-
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

class PokerPlayer():

    def __init__(self, number, fund=10000):
        self.playernumber = number
        self.fundation = fund
        self.cardlist = []
        self.status = 0
        self.currbet = 0
        self.gamebet = 0
        self.ingame = True

    def playGame(self):
        pass

    def quitGame(self):
        self.ingame = False