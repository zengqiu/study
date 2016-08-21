#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Web 的套接字函数库 urllib2

import urllib2

url = "http://www.v2ex.com"

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)

print response.read()
response.close()