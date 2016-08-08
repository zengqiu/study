# -*- coding: utf-8 -*-

# 把套接字改成阻塞或非阻塞模式

import socket

def test_socket_modes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 1    阻塞模式
    # 0    非阻塞模式
    s.setblocking(1)
    
    s.settimeout(0.5)
    s.bind(("127.0.0.1", 0))

    socket_address = s.getsockname()
    print "Trivial Server launched on socket: %s" % str(socket_address)
    while(1):
        s.listen(1)

if __name__ == '__main__':
    test_socket_modes()