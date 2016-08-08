# -*- coding: utf-8 -*-

# 将 IPv4 地址转换成不同的格式

# socket.inet_aton()    将一个字符串 IP 地址转换为一个 32 位的网络序列IP地址
# socket.inet_ntoa()    将一个十进制网络字节序转换为点分十进制 IP 格式的字符串

import socket
from binascii import hexlify

def convert_ipv4_address():
    for ip_addr in ['127.0.0.1', '192.168.0.1']:
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print "IP address: %s => packed: %s, unpacked: %s" % (ip_addr, hexlify(packed_ip_addr), unpacked_ip_addr)

if __name__ == '__main__':
    convert_ipv4_address()