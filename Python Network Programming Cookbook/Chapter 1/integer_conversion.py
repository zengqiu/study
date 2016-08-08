# -*- coding: utf-8 -*-

# 主机字节序和网络字节序之间相互转换

# socket.ntohl()    将一个无符号长整形数从网络字节序转换为长整形主机字节序
# socket.ntohs()    将一个无符号短整形数从网络字节序转换为短整形主机字节序

import socket

def convert_integer():
    data = 1234
    # 32-bit
    print "Original: %s => Long host byte order: %s, Network byte order: %s" % (data, socket.ntohl(data), socket.htonl(data))
    # 16-bit
    print "Original: %s => Short host byte order: %s, Network byte order: %s" % (data, socket.ntohs(data), socket.htons(data))

if __name__ == '__main__':
    convert_integer()