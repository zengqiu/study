# -*- coding: utf-8 -*-

# 通过代理服务器发送 Web 请求

import urllib

URL = 'https://www.github.com'
PROXY_ADDRESS = '1.164.144.107:8080'    # Get from http://www.xicidaili.com/

if __name__ == '__main__':
    resp = urllib.urlopen(URL, proxies = {"http": PROXY_ADDRESS})
    print "Proxy server returns response headers: %s" % resp.headers