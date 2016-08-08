# -*- coding: utf-8 -*-

# 编写一个 IPv6 回显客户端/服务器（客户端）

import argparse
import socket
import sys

HOST = 'localhost'
BUFSIZE = 1024

def ipv6_echo_client(port, host=HOST):
    for result in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = result
        print sa
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error, err:
            print "Error: %s" % err

        try:
            sock.connect(sa)
        except socket.error, err:
            print err
            sock.close()
            continue

    if sock is None:
        print 'Failed to open socket!'
        sys.exit(1)

    msg = "Hello from ipv6 client"
    print "Send data to server: %s" % msg
    sock.send(msg)
    
    while True:
        data = sock.recv(BUFSIZE)
        print "Received from server: [%s]" % data
        if not data:
            break
    sock.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPv6 Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    ipv6_echo_client(port)