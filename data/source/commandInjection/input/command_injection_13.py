#
#

import socket
import subprocess
import re

def sanitize_input(command):
    return re.sub(r'[^\w\s]', '', command)

def execute_command(command):
    try:
        sanitized_command = sanitize_input(command)
        result = subprocess.check_output(sanitized_command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e)

def start_server(host='localhost', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                response = execute_command(data)
                conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()