# -*- coding: utf-8 -*-

# 使用 CGI 为基于 Python 的 Web 服务器编写一个留言板（服务器）

import os
import cgi
import argparse
import BaseHTTPServer
import CGIHTTPServer
import cgitb

cgitb.enable()    # Enable CGI error reporting

def web_server(port):
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler    # RequestsHandler
    server_address = ("", port)
    handler.cgi_directories = ["/cgi-bin", ]
    httpd = server(server_address, handler)
    print "Starting web server with CGI support on port: %s ..." % port
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CGI Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    web_server(given_args.port)