# -*- coding: utf8 -*-
import os
import sys
import time
import socket
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("../..")
from base_py._baseexecuteoperate import *

class SocketBase(object):
    _DefaultHost = 'localhost'
    _DefaultPort = 8001
    _DefaultTransMaxSize = 1024
    _DefaultEndPattern = 'END'
    _host = None
    _port = None
    _sock = None
    def __init__(self):
        super(SocketBase, self).__init__()
        argdict = self.LoadParamArguments()
        self._host = argdict['host']
        self._port = tryConvertData(argdict['port'], int, self._DefaultPort)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def LoadParamArguments(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-s', '--host', default=self._DefaultHost,
            dest='host', help='host server address')
        argparser.add_argument('-p', '--port', default=str(self._DefaultPort),
            dest='port', help='host server use port')
        args = argparser.parse_args()
        paramdict = dict()
        paramdict['host'] = getattr(args, 'host', None)
        paramdict['port'] = getattr(args, 'port', None)
        return paramdict

    def DealSendData(self, connecthandler, senddata, isend=True):
        datasize = len(senddata)
        cursize = 0
        cursenddata = ""
        while cursize < datasize:
            if cursize + self._DefaultTransMaxSize >= datasize:
                cursenddata = senddata[cursize:datasize]
            else:
                cursenddata = senddata[cursize:cursize+self._DefaultTransMaxSize]
            connecthandler.send(cursenddata)
            print "send data: %s" % cursenddata
            cursize += self._DefaultTransMaxSize
        if isend is True:
            print "send data end"
            connecthandler.send(self._DefaultEndPattern)

    def DealRecvData(self, connecthandler):
        recvdata = ""
        databuf = ''
        while not databuf == self._DefaultEndPattern:
            databuf = connecthandler.recv(self._DefaultTransMaxSize)
            print "recv data: %s" % (databuf)
            recvdata += databuf
        return recvdata

if __name__ == '__main__' :
    try:
        sockop = SocketBase()
    except Exception as e:
        print e
        raise