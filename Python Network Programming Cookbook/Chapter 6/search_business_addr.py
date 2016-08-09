# -*- coding: utf-8 -*-

# 使用谷歌地图 API 搜索公司地址

from pygeocoder import Geocoder

def search_business(business_name):
    results = Geocoder.geocode(business_name)
    
    for result in results:
        print result

if __name__ == '__main__':
    business_name =  "Argos Ltd, London" 
    print "Searching %s" % business_name
    search_business(business_name)  