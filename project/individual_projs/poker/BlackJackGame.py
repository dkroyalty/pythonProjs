# -*- coding: utf-8 -*-
import sys
from BlackJackPlayer import BlackJackPlayer
from PokerGame import PokerGame

reload(sys)
sys.setdefaultencoding('utf-8')

class BlackJackGame(PokerGame):

    def __init__(self, playersize=4, cardsetnum=4):
        assert playersize > 1
        self.bankerid = 0
        PokerGame.__init__(self, cardsetnum, True)
        for i in range(playersize):
            self.playerlist.append(BlackJackPlayer(i, 10000, i==self.bankerid))

    def dealInGamePlayerCard(self):
        PokerGame.dealInGamePlayerCard(self)
        for eachplayer in self.playerlist:
            if eachplayer.status == BlackJackPlayer.Hit:
                if len(eachplayer.cardlist) > 0:
                    self.dealCard(eachplayer.playernumber, 1)
                else:
                    self.dealCard(eachplayer.playernumber, 2)

    def checkOneLoopEnd(self):
        oneLoopEnd = True
        for eachplayer in self.playerlist:
            if eachplayer.status == BlackJackPlayer.Hit:
                oneLoopEnd = False
                break
        return oneLoopEnd

    def balanceResult(self):
        PokerGame.balanceResult(self)
        if self.checkOneLoopEnd() == True:
            for eachplayer in self.playerlist:
                if not eachplayer.playernumber == self.bankerid:
                    betvalue = self.getBetValue(eachplayer.playernumber, self.bankerid)
                    comprst = self.getCompareResult(eachplayer.playernumber, self.bankerid)
                    if comprst == 0:
                        eachplayer.fundation -= betvalue
                        self.playerlist[self.bankerid].fundation += betvalue
                    elif comprst == 1:
                        eachplayer.fundation += betvalue
                        self.playerlist[self.bankerid].fundation -= betvalue
            self.forceend = True
            self.reportGameStatus()
            self.resetPlayerStatus()

    def getBetValue(self, playernum, bankernum):
        assert not playernum == bankernum
        betvalue = self.playerlist[playernum].currbet
        playerbj = self.playerlist[playernum].isBlackJack()
        bankerbj = self.playerlist[bankernum].isBlackJack()
        if (playerbj or bankerbj) and not (playerbj and bankerbj):
            betvalue *= 2
        return betvalue

    def getCompareResult(self, playernum, bankernum):
        assert not playernum == bankernum
        bankerbj = self.playerlist[bankernum].isBlackJack()
        playerbj = self.playerlist[playernum].isBlackJack()
        bankerbust = self.playerlist[bankernum].isBust()
        playerbust = self.playerlist[playernum].isBust()
        if bankerbj == True and playerbj == True:
            return -1
        elif bankerbj == True and playerbj == False:
            return 0
        elif bankerbj == False and playerbj == True:
            return 1
        else:
            if playerbust == True:
                return 0
            elif bankerbust == True:
                return 1
            else:
                bankervalue = self.playerlist[bankernum].calculateTotalValue()
                playervalue = self.playerlist[playernum].calculateTotalValue()
                if bankervalue == playervalue:
                    return -1
                elif bankervalue > playervalue:
                    return 0
                else:
                    return 1
        return -1

    def reportGameStatus(self):
        print PokerGame.getStatusInfo(self)
        for eachplayer in self.playerlist:
            if hasattr(eachplayer, 'getStatusInfo'):
                print eachplayer.getStatusInfo()
        print "Banker is player %d" % (self.bankerid)

if __name__ == "__main__":
    testGame = BlackJackGame()
    testGame.gameLoop()
