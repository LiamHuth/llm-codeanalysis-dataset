#
#

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        file_path = unquote(parsed_path.path)
        if ".." in file_path or file_path.startswith('/'):
            self.send_response(403)
            self.end_headers()
            return
        with open(file_path, 'rb') as file:
            self.send_response(200)
            self.wfile.write(file.read())

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), Server)
    server.serve_forever()
