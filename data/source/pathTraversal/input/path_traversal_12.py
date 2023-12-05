#
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse, unquote

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        parsed_path = urlparse(path)
        query = parsed_path.query
        unsanitized_path = unquote(parsed_path.path)
        sanitized_path = os.path.normpath(unsanitized_path)
        final_path = unsanitized_path if sanitized_path == "/" else sanitized_path

        if final_path == "/":
            final_path = "./public/index.html"

        if 'file=' in query:
            final_path = unquote(query.split('file=')[1])

        filePath = os.path.join(os.getcwd(), final_path)
        try:
            with open(filePath, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: %s' % path)

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
