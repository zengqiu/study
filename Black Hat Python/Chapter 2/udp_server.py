# -*- coding: utf-8 -*-

# UDP 服务器

import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((bind_ip, bind_port))
print "[*] Listening on %s:%d" % (bind_ip, bind_port)

while True:
    # 打印出客户端发送得到内容
    data, addr = server.recvfrom(4096)
    print "[*] Received: %s" % data
    # 返还一个数据包
    server.sendto("OK!", addr)