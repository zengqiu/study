# -*- coding: utf-8 -*-

# 探测设备中的接口是否开启

import argparse
import socket
import fcntl
import struct
import nmap

SAMPLE_PORT = '21-23'
SIOCGIFADDR = 0x8915

def get_interface_status(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', ifname[:15]))[20:24])
    nm = nmap.PortScanner()
    nm.scan(ip_address, SAMPLE_PORT)
    print nm[ip_address]
    return nm[ip_address].state()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Networking Utils')
    parser.add_argument('--ifname', action='store', dest='ifname', required=True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    print "Interface [%s] --> IP: %s" % (ifname, get_interface_status(ifname))