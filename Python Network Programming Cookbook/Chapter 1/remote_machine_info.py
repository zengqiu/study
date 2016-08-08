# -*- coding: utf-8 -*-

# 获取远程设备的 IP 地址

import socket

def get_remote_machine_info():
    remote_host = 'www.079l.com'
    try:
        print "IP address: %s" % socket.gethostbyname(remote_host)
        print socket.gethostbyname_ex(remote_host)
    except socket.error, err_msg:
        print "%s: %s" % (remote_host, err_msg)

if __name__ == '__main__':
    get_remote_machine_info()