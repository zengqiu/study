# -*- coding: utf-8 -*-

# 使用谷歌地图 URL 搜索地理坐标

import argparse
import os
import urllib
import xml.etree.ElementTree as ET
from xml.dom import minidom

# https://developers.google.com/maps/documentation/geocoding/get-api-key
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

def find_lat_long(city):
        """Find geographic coordinates"""
        # Encode query string into Google maps URL
        
        url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + city + '&key=' + GOOGLE_MAPS_API_KEY
        print 'Query: %s' % (url)
    
        # Get XML location from Google maps
        xml_str = urllib.urlopen(url).read()
        xml_doc = minidom.parseString(xml_str)
    
        if xml_doc.getElementsByTagName('status')[0].firstChild.nodeValue != 'OK':
            print '\nGoogle cannot interpret the city.'
            return
        else:
            # 默认取第一个数据
            lat = xml_doc.getElementsByTagName('lat')[0].firstChild.nodeValue
            lng = xml_doc.getElementsByTagName('lng')[0].firstChild.nodeValue
            print "Latitude/Longitude: %s/%s\n" % (lat, lng)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='City Geocode Search')
    parser.add_argument('--city', action="store", dest="city", required=True)
    given_args = parser.parse_args()
    
    print "Finding geographic coordinates of %s" % given_args.city
    find_lat_long(given_args.city)