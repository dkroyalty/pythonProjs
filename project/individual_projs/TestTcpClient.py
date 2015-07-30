# -*- coding : utf8 -*-
import socket

s = socket.socket()
server = '127.0.0.1'#socket.gethostname()
port = 1234
addr = (server, port)
print addr
s.connect(addr)
s.send('123456')
print s.recv(1024)
s.send('654321')
print s.recv(1024)
s.close


