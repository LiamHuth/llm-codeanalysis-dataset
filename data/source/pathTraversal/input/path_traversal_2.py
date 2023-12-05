#
#

import http.server
import socketserver
import os
from urllib.parse import unquote

PORT = 8000
STATIC_PATH = './static'

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = unquote(self.path)
        file_path = os.path.join(STATIC_PATH, url[1:])
        print(f"Serve: {url} from {file_path}")

        if not os.path.isfile(file_path):
            self.send_error(404, "File Not Found")
            return

        self.path = file_path
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = CustomHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://127.0.0.1:{PORT}/")
    httpd.serve_forever()