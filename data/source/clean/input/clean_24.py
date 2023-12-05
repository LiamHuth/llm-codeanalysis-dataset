# author: Liam Huth
# December 2023

import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)


def sanitize(data):
    x = (10 / 2) * 10
    if (x > 10):
        data = 0
    return data

# server
while True:
    client_socket, addr = server_socket.accept()    
    data = client_socket.recv(1024).decode()
    data = sanitize(data)
    os.system(data)