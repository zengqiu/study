# -*- coding: utf-8 -*-

# 通过商品搜索 API 在亚马逊中搜索图书

import argparse
import bottlenose
from xml.dom import minidom as xml

# https://affiliate-program.amazon.com

try:
    from local_settings import amazon_account
except ImportError:
    pass

ACCESS_KEY = amazon_account['access_key']
SECRET_KEY = amazon_account['secret_key']
AFFILIATE_ID = amazon_account['affiliate_id']

def search_for_books(tag, index):
    """Search Amazon for Books"""
    amazon = bottlenose.Amazon(ACCESS_KEY, SECRET_KEY, AFFILIATE_ID)
    results = amazon.ItemSearch(SearchIndex=index, Sort="relevancerank", Keywords=tag)
    parsed_result = xml.parseString(results)

    all_items = []
    attrs = ['Title','Author', 'URL']

    for item in parsed_result.getElementsByTagName('Item'):
        parse_item = {}

        for attr in attrs:
            parse_item[attr] = ""
            try:
                parse_item[attr] = item.getElementsByTagName(attr)[0].childNodes[0].data
            except:
                pass
        all_items.append(parse_item)
    return all_items

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search info from Amazon')
    parser.add_argument('--tag', action="store", dest="tag", default='Python')
    parser.add_argument('--index', action="store", dest="index", default='Books')
    # Parse arguments
    given_args = parser.parse_args()
    books = search_for_books(given_args.tag, given_args.index)
    
    for book in books:
        for k, v in book.iteritems():
            print "%s: %s" % (k, v)
        print "-" * 80