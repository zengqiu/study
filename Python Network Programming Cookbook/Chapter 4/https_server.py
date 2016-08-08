# -*- coding: utf-8 -*-

# 使用 Python 和 OpenSSL 编写一个简单的 HTTPS 服务器

import socket
import os
import sys
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL, crypto
from random import random

TARGET_URL = 'http://www.python.org/ftp/python/2.7.4/'
TARGET_FILE = 'Python-2.7.4.tgz'

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)

        ctx = SSL.Context(SSL.SSLv23_METHOD)
        
        # Location of the server private key and the server certificate
        # 生成两个证书
        # openssl req -x509 -newkey rsa:2048 -keyout pkey.pem -out cert.pem -days 365
        # ctx.use_privatekey_file('pkey.pem')
        # ctx.use_certificate_file('cert.pem')

        # 生成一个证书
        # openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
        fpem = 'server.pem'
        ctx.use_privatekey_file(fpem)
        ctx.use_certificate_file(fpem)
        
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()

    def shutdown_request(self, request):
        request.shutdown()

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        """Handler for the GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the message to browser
        self.wfile.write("Hello from https server!")
        return

def run_server(HandlerClass=SecureHTTPRequestHandler, ServerClass=SecureHTTPServer):
    server_address = ('', 4443)    # port needs to be accessible by user
    server = ServerClass(server_address, HandlerClass)
    running_address = server.socket.getsockname()
    print "Serving HTTPS Server on %s:%s ..." % (running_address[0], running_address[1])
    server.serve_forever()

if __name__ == '__main__':
    run_server()