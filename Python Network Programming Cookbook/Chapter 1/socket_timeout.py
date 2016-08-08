# -*- coding: utf-8 -*-

# 设定并获取默认的套接字超时时间

import socket

def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Default socket timeout: %s" % s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout: %s" % s.gettimeout()

if __name__ == '__main__':
    test_socket_timeout()