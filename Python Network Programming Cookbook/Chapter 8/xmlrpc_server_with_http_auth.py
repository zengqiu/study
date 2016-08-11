# -*- coding: utf-8 -*-

# 运行一个支持 HTTP 基本认证的 XML-RPC 服务器（服务端）

import argparse
import xmlrpclib
from base64 import b64decode
from SimpleXMLRPCServer  import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

class SecureXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, host, port, username, password, *args, **kargs):
        self.username = username
        self.password = password
        # Authenticate method is called from inner class
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
              # Method to override
              def parse_request(request):
                  if SimpleXMLRPCRequestHandler.parse_request(request):
                      # Authenticate
                      if self.authenticate(request.headers):
                          return True
                      else:
                          # If authentication fails return 401
                          request.send_error(401, 'Authentication failed, Try agin.')
                  return False
        # Initialize
        SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=VerifyingRequestHandler, *args, **kargs)

    def authenticate(self, headers):
        print headers
        headers = headers.get('Authorization').split()
        print headers
        basic, encoded = headers[0], headers[1]
        if basic != 'Basic':
            print 'Only basic authentication supported'
            return False
        secret = b64decode(encoded).split(':')
        username, password = secret[0], secret[1]
        return True if (username == self.username and password == self.password) else False

def run_server(host, port, username, password):
    server = SecureXMLRPCServer(host, port, username, password)
    # Simple test function
    def echo(msg):
        """Reply client in  uppser case"""
        reply = msg.upper()
        print "Client said: %s. So we echo that in uppercase: %s" % (msg, reply)
        return reply
    server.register_function(echo, 'echo')
    print "Running a HTTP auth enabled XMLRPC server on %s:%s..." % (host, port)
    server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded multicall XMLRPC Server/Proxy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8000, type=int)
    parser.add_argument('--username', action="store", dest="username", default='user')
    parser.add_argument('--password', action="store", dest="password", default='pass')
    # Parse arguments
    given_args = parser.parse_args()
    host, port =  given_args.host, given_args.port
    username, password = given_args.username, given_args.password
    run_server(host, port, username, password)