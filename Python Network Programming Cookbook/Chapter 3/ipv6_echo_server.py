# -*- coding: utf-8 -*-

# 编写一个 IPv6 回显客户端/服务器（服务器）

import argparse
import socket
import sys

HOST = 'localhost'

def echo_server(port, host=HOST):
    """Echo server using IPv6"""
    for result in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = result

        # 过滤回环接口
        if sa[0] == '::1':
            continue
            
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error, err:
            print "Error: %s" % err

        try:
            sock.bind(sa)
            sock.listen(1)
            print "Server listening on %s:%s" % (host, port)
        except socket.error, err:
            sock.close()
            continue
        break
        sys.exit(1)
    conn, addr = sock.accept()
    print 'Connected to: ', addr
    while True:
        data = conn.recv(1024)
        print "Received data from the client: [%s]" % data
        if not data:
            break
        conn.send(data)
        print "Sent data echoed back to the client: [%s]" % data
    conn.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPv6 Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)