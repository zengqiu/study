# -*- coding: utf-8 -*-

# 在你的设备中伺服 HTTP 请求

import argparse
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800

class RequestHandler(BaseHTTPRequestHandler):
    """Custom request handler"""
    def do_GET(self):
        """Handler for the GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the message to browser
        self.wfile.write("Hello from server!")
        return

class CustomHTTPServer(HTTPServer):
    """A custom HTTP server"""
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, RequestHandler)

def run_server(port):
    try:
        server = CustomHTTPServer(DEFAULT_HOST, port)
        print "Custom HTTP server started on port: %s" % port
        server.serve_forever()
    except Exception, err:
        print "Error: %s" % err
    except KeyboardInterrupt:
        print "Server interrupted and is shutting down..."
        server.socket.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple HTTP Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    run_server(port)