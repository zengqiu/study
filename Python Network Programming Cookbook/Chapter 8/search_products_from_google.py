# -*- coding: utf-8 -*-

# 使用谷歌搜索定制信息

import argparse
import json
import urllib
import requests

# https://cse.google.com/all
# https://console.developers.google.com/flows/enableapi?apiid=customsearch&credential=client_key

try:
    from local_settings import google_custom_search_api
except ImportError:
    pass

key = google_custom_search_api['key']
cx = google_custom_search_api['cx']

BASE_URL = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=' % (key, cx)

def get_search_url(query):
    return "%s%s" % (BASE_URL, query)

def search_info(tag):
    query = urllib.urlencode({'q': tag})
    url = get_search_url(query)
    response = requests.get(url)
    results = response.json()
    
    print 'Found total results: %s' % results['searchInformation']['totalResults']
    hits = results['items']
    print 'Found top %d hits:' % len(hits)
    for h in hits:
        print ' ', h['link']
    print 'More results available from %s&start=%s' % (get_search_url(query), str(results['queries']['nextPage'][0]['startIndex']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search info from Google')
    parser.add_argument('--tag', action="store", dest="tag", default='Python books')
    # Parse arguments
    given_args = parser.parse_args()
    search_info(given_args.tag)