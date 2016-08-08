# -*- coding: utf-8 -*-

# 使用相连的套接字执行基本的进程间通信

import socket
import os

BUFSIZE = 1024

def test_socketpair():
    """Test Unix socketpair"""
    parent, child = socket.socketpair()
    pid = os.fork()
    try:
        if pid:
            print "@Parent, sending message..."
            child.close()
            parent.sendall("Hello from parent!")
            response = parent.recv(BUFSIZE)
            print "Response from child: ", response
            parent.close()
        else:
            print "@Child, waiting for message from parent"
            parent.close()
            message = child.recv(BUFSIZE)
            print "Message from parent: ", message
            child.sendall("Hello from child!")
            child.close()
    except Exception, err:
        print "Error: %s" % err
    
if __name__ == '__main__':
    test_socketpair()