# -*- coding: utf-8 -*-

# UDP 客户端

import socket

target_host = '127.0.0.1'
target_port = 9999

# 建立一个 socket 对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 发送一些数据
client.sendto("AAABBBCCC", (target_host, target_port))
# 接收一些数据
data, addr = client.recvfrom(4096)
print data