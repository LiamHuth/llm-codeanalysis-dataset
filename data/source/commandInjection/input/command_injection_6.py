# author: Liam Huth
# December 2023

import socket
import sys

def update_sys_path(new_path):
    if new_path not in sys.path:
        sys.path.insert(0, new_path)
        return f"Path updated. New sys.path: {sys.path}"
    return f"Path already in sys.path: {sys.path}"

def start_server(host='localhost', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                response = update_sys_path(data.decode())
                conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()