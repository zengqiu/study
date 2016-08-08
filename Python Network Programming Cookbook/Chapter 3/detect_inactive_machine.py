# -*- coding: utf-8 -*-

# 检测网络中未开启的设备

import argparse
import time
import sched
from scapy.all import sr, srp, IP, UDP, ICMP, TCP, ARP, Ether

RUN_FREQUENCY = 10

scheduler = sched.scheduler(time.time, time.sleep)

def detect_inactive_hosts(scan_hosts):
    """Scan the network to find scan_hosts are live or dead
    scan_hosts can be like 10.0.2.2-4 to cover range
    See scapy docs for specifying target"""
    global scheduler
    # schedule.enter(delay, priority, action, (argument1,  ))
    # dealy 延迟时间
    # priority 优先级（用于同时间到达的两个事件同时执行时定序）
    # action 回调函数（被调用触发的函数）
    # argument1 回调函数参数
    # scheduler.enter(RUN_FREQUENCY, 1, detect_inactive_hosts, (scan_hosts, ))
    inactive_hosts = []
    try:
        # sr 返回有回应的数据包和没有回应的数据包
        ans, unans = sr(IP(dst=scan_hosts)/ICMP(), retry=0, timeout=1)
        ans.summary(lambda(s, r): r.sprintf("%IP.src% is alive"))
        for inactive in unans:
            print "%s is inactive" % inactive.dst
            inactive_hosts.append(inactive.dst)
        print "Total %d hosts are inactive" % (len(inactive_hosts))
    except KeyboardInterrupt:
        exit(0)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Networking Utils')
    parser.add_argument('--scan-hosts', action='store', dest='scan_hosts', required=True)
    given_args = parser.parse_args()
    scan_hosts = given_args.scan_hosts
    scheduler.enter(1, 1, detect_inactive_hosts, (scan_hosts, ))
    scheduler.run()