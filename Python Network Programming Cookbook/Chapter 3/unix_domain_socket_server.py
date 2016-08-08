# -*- coding: utf-8 -*-

# 使用 Unix 域套接字执行进程间通信（服务端）

import socket
import os
import time

SERVER_PATH = "/tmp/python_unix_socket_server"

def run_unix_domain_socket_server():
    if os.path.exists(SERVER_PATH):
        os.remove(SERVER_PATH)

    print "Starting unix domain socket server"
    
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)    # TCP
    server.bind(SERVER_PATH)
    server.listen(5)    # TCP

    print "Listening on path: %s" % SERVER_PATH
    while True:
        conn, addr = server.accept()    # TCP
        datagram = conn.recv(1024)    # TCP
        if not datagram:
            break
        else:
            print "-" * 20
            print datagram
            conn.sendall(datagram)    # TCP
        if "DONE" == datagram:
            break
    print "-" * 20
    print "Server is shutting down now..."
    server.close()
    os.remove(SERVER_PATH)
    print "Server shutdown and path removed"
    
if __name__ == '__main__':
    run_unix_domain_socket_server()