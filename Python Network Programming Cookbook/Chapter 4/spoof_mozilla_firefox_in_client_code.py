# -*- coding: utf-8 -*-

# 把客户端伪装成 Mozilla Firefox

import urllib2

BROWSER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'
URL = 'http://www.python.org'

def spoof_firefox():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', BROWSER)]
    result = opener.open(URL)
    print "Response headers:"
    for header in result.headers.headers:
        print "\t", header

if __name__ == '__main__':
    spoof_firefox()