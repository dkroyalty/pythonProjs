# -*- coding : utf8 -*-
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 1234)
print >>sys.stderr, 'starting up on %s port %s ' %server_address
sock.bind(server_address)

sock.listen(2)

while True:
    print 'waiting for a connection....'
    connection, client_address = sock.accept()
    print 'connection from', client_address
    while True:
        try:
            data = connection.recv(1024).strip()
            print 'received "%s"' %data
            if data:
                print 'sending data back to the client'
                connection.sendall('received data: '+ data+'\n')
            else:
                print 'disconnect for no data from', client_address
                connection.close()
                break
        except:
            print 'connection closed'
            connection.close()
            break


# from SocketServer import TCPServer, BaseRequestHandler

# class MyBaseRequestHandlerr(BaseRequestHandler):
#     def handle(self):
#         while True:
#             try:
#                 data = self.request.recv(1024).strip()
#                 print "receive from (%r):%r" % (self.client_address, data)
#                 self.request.sendall(data.upper())
#             except:
#                 print "lost connection"
#                 break

# if __name__ == "__main__":
#     host = "127.0.0.1"
#     port = 1234
#     addr = (host, port)
#     print addr
#     server = TCPServer(addr, MyBaseRequestHandlerr)
#     server.serve_forever()