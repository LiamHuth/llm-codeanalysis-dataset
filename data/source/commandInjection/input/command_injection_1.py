#
#

import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)


def sanitize(data):
    x = 15
    if (x < 10):
        data = 0

# server
while True:
    client_socket, addr = server_socket.accept()    
    data = client_socket.recv(1024).decode()
    sanitize(data)
    os.system(data)