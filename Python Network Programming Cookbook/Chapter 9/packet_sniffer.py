# -*- coding: utf-8 -*-

# 嗅探网络数据包

# pylibpcap-0.6.4 BUG:
#     pcap.c: In function ‘SWIG_Python_AddErrorMsg’:
#     pcap.c:853:5: error: format not a string literal and no format arguments [-Werror=format-security]
#          PyErr_Format(PyExc_RuntimeError, mesg);
#          ^~~~~~~~~~~~
#     cc1: some warnings being treated as errors
#     error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
# Solution:
#     File --- ./pylibpcap-0.6.4/pcap.c
#     Edit line 853 --- // PyErr_Format(PyExc_RuntimeError, mesg);

import argparse
import pcap
from construct.protocols.ipstack import ip_stack

def print_packet(pktlen, data, timestamp):
    """Callback for priniting the packet payload"""
    if not data:
        return
    
    stack = ip_stack.parse(data)
    payload = stack.next.next.next
    print payload

def main():
    # Setup commandline arguments
    parser = argparse.ArgumentParser(description='Packet Sniffer')
    parser.add_argument('--iface', action="store", dest="iface", default='enp0s3')
    parser.add_argument('--port', action="store", dest="port", default=80, type=int)
    # Parse arguments
    given_args = parser.parse_args()
    iface, port = given_args.iface, given_args.port
    # Start sniffing
    pc = pcap.pcapObject()
    pc.open_live(iface, 1600, 0, 100)
    pc.setfilter('dst port %d' % port, 0, 0)
    
    print 'Press CTRL+C to end capture'
    try:
        while True:
            pc.dispatch(1, print_packet)
    except KeyboardInterrupt:
        print 'Packet statistics: %d packets received, %d packets dropped, %d packets dropped by the interface' % pc.stats()

if __name__ == '__main__':
    main()