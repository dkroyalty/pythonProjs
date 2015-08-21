# -*- coding: utf8 -*-
import sys
import time
from socketBase import SocketBase

reload(sys)
sys.setdefaultencoding('utf-8')

class SocketClient(SocketBase):
    def __init__(self):
        super(SocketClient, self).__init__()

    def StartClient(self):
        try :
            self._sock.connect((self._host, self._port))
        except Exception as e:
            print e
        inputdata = ''
        while self.OperateClient(inputdata) is True:
            inputdata = raw_input("input command: ")
        self._sock.close()

    def OperateClient(self, clientcmd):
        if clientcmd == 'exit':
            return False
        if len(clientcmd) > 0:
            self.DealSendData(self._sock, clientcmd)
            print "[receive from server]:"
            print self.DealRecvData(self._sock)
            print "[receive end ========]"
        return True

if __name__ == '__main__' :
    try:
        sockclient = SocketClient()
        sockclient.StartClient()
    except Exception as e:
        print e
        raise