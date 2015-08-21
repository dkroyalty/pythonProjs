# -*- coding: utf8 -*-
import os
import sys
import time
from socketBase import SocketBase

reload(sys)
sys.setdefaultencoding('utf-8')

class SocketServer(SocketBase):
    _DefaultMaxConnection = 100
    _DefaultTimeout = 5
    def __init__(self):
        super(SocketServer, self).__init__()

    def StartServer(self):
        try :
            self._sock.bind((self._host, self._port))
            self._sock.listen(self._DefaultMaxConnection)
        except :
            print >> sys.stderr, u'failed to bind server port'
            self._sock.close()
            raise
        print "run at %s:%d" % (self._host, self._port)
        self.OperateServer()
        self._sock.close()

    def OperateServer(self):
        while True:
            acceptstate = True
            connection = None
            try:
                connection, address = self._sock.accept()
                #connection.settimeout(self._DefaultTimeout)
                clientaddr = '%s:%d' % (address[0], address[-1])
                print "create connection from %s" % (clientaddr)
            except Exception as e:
                print e
                acceptstate = False
            while acceptstate:
                try:
                    databuf = self.DealRecvData(connection)
                    self.OperateWithData(connection, databuf)
                except Exception as e:
                    print e
                    break
            print "close connection to %s" % (clientaddr)
            if connection is not None:
                connection.close()

    def OperateWithData(self, connecthandler, databuf):
        path = os.getcwd()
        filelist = os.listdir(path)
        filestr = ','.join(filelist)
        retdata = "[data]%s[size]%d" % (databuf, len(databuf))
        retdata += "\npath:\n%s\nfiles:%s" % (path, filestr)
        self.DealSendData(connecthandler, retdata)

if __name__ == '__main__' :
    try:
        sockclient = SocketServer()
        sockclient.StartServer()
    except Exception as e:
        print e
        raise
