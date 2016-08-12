# -*- coding: utf-8 -*-

# 扫描数据包的广播

from scapy.all import *
import os

captured_data = dict()

END_PORT = 1000

def monitor_packet(pkt):
    if IP in pkt:
        if not captured_data.has_key(pkt[IP].src):
            captured_data[pkt[IP].src] = []

    if TCP in pkt:
        if pkt[TCP].sport <=  END_PORT:
            if not str(pkt[TCP].sport) in captured_data[pkt[IP].src]:
                captured_data[pkt[IP].src].append(str(pkt[TCP].sport))

    os.system('clear')
    ip_list = sorted(captured_data.keys())
    for key in ip_list:
        ports=', '.join(captured_data[key])
        if len(captured_data[key]) == 0:
            print '%s' % key
        else:
            print '%s (%s)' % (key, ports)

if __name__ == '__main__':
    sniff(prn=monitor_packet, store=0)