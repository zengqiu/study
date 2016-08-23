#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 通过 Paramiko 使用 SSH（服务端）

import sys
import socket
import threading
import paramiko

# 使用 Paramiko 示例文件的密匙
# https://github.com/paramiko/paramiko/tree/master/demos
host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
            
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if username == 'mini' and password == 'zengqiu':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Listening for connection...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen failed: ' + str(e)
    sys.exit(1)
    
print '[+] Got a connection!'

try:
    bh_session = paramiko.Transport(client)
    bh_session.add_server_key(host_key)
    server = Server()
    
    try:
        bh_session.start_server(server=server)
    except paramiko.SSHException, e:
        print '[-] SSH negotiation failed.'
        
    chan = bh_session.accept(20)
    print '[+] Authenticated!'
    print chan.recv(1024)
    chan.send('Welcome to bh_ssh')
    
    while True:
        try:
            command = raw_input("Enter command: ").strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bh_session.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bh_session.close()
except Exception, e:
    print '[-] Caught exception: ' + str(e)
    try:
        bh_session.close()
    except:
        pass
        
    sys.exit(1)