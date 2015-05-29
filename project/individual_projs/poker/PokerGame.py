# -*- coding: utf-8 -*-
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

class PokerGame():

    def __init__(self):
        self.playerlist = []
        self.counter = 0
        self.forceend = False

    def gameLoop(self):
        while self.checkGameEnd() == False:
            self.runOneLoopGame()
            self.balanceResult()
            self.counter += 1

    def runOneLoopGame(self):
        assert len(self.playerlist) > 0
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'playGame'):
                eachplayer.playGame()

    def checkGameEnd(self):
        assert len(self.playerlist) > 0
        if self.forceend == True:
            return True
        playercounter = 0
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'ingame'):
                if eachplayer.ingame == True:
                    playercounter += 1
        return playercounter > 1

    def balanceResult(self):
        pass