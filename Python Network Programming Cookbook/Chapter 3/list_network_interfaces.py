# -*- coding: utf-8 -*-

# 枚举设备中的接口

import sys
import socket
import fcntl
import struct
import array

SIOCGIFCONF = 0x8912    # from C library sockios.h
STRUCT_SIZE_32 = 32
STRUCT_SIZE_64 = 40
PLATFORM_32_MAX_NUMBER = 2**32
DEFAULT_INTERFACES = 1

def list_interfaces():
    interfaces = []
    max_interfaces = DEFAULT_INTERFACES
    is_64bit = sys.maxsize > PLATFORM_32_MAX_NUMBER
    struct_size = STRUCT_SIZE_64 if is_64bit else STRUCT_SIZE_32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        bytes = max_interfaces * struct_size
        interface_names = array.array('B', '\0'*bytes)
        # buffer_info() -> (address, length)    返回当前内存地址和数组长度
        sock_info = fcntl.ioctl(sock.fileno(), SIOCGIFCONF, struct.pack('iL', bytes, interface_names.buffer_info()[0]))
        outbytes = struct.unpack('iL', sock_info)[0]
        if outbytes == bytes:
            max_interfaces *= 2
        else:
            break
    namestr = interface_names.tostring()
    for i in range(0, outbytes, struct_size):
        interfaces.append((namestr[i:i+16].split('\0', 1)[0]))
    return interfaces
    
if __name__ == '__main__':
    interfaces = list_interfaces()
    print "The machine has %s network interfaces: %s." % (len(interfaces), interfaces)