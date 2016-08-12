# -*- coding: utf-8 -*-

# 读取保存的 pcap 文件以重放流量

import argparse
from scapy.all import *

def send_packet(recvd_pkt, src_ip, dst_ip, count):
    """Send modified packets"""
    pkt_cnt = 0
    p_out = []

    for p in recvd_pkt:
        pkt_cnt += 1
        new_pkt = p.payload
        new_pkt[IP].dst = dst_ip
        new_pkt[IP].src = src_ip
        del new_pkt[IP].chksum
        p_out.append(new_pkt)
        if pkt_cnt % count == 0:
            send(PacketList(p_out))
            p_out = []

    # Send rest of packet
    send(PacketList(p_out))
    print "Total packets sent: %d" % pkt_cnt

if __name__ == '__main__':
    # Setup commandline arguments
    parser = argparse.ArgumentParser(description='Packet Sniffer')
    parser.add_argument('--infile', action="store", dest="infile", default='pcap1.pcap')
    parser.add_argument('--src-ip', action="store", dest="src_ip", default='1.1.1.1')
    parser.add_argument('--dst-ip', action="store", dest="dst_ip", default='2.2.2.2')
    parser.add_argument('--count', action="store", dest="count", default=100, type=int)
    # Parse arguments
    given_args = parser.parse_args()
    global src_ip, dst_ip
    infile = given_args.infile
    src_ip = given_args.src_ip
    dst_ip = given_args.dst_ip
    count = given_args.count
    try:
        pkt_reader = PcapReader(infile)
        send_packet(pkt_reader, src_ip, dst_ip, count)
    except IOError:
        print "Failed reading file %s contents" % infile
        sys.exit(1)