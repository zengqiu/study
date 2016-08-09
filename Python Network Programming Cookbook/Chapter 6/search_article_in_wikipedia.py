# -*- coding: utf-8 -*-

# 搜索维基百科中的文章

import argparse
import re
import urllib
import urllib2
import json
import sys

SEARCH_URL = 'http://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&sroffset=%d&srlimit=%d&format=json'

class Wikipedia:
    def __init__(self, lang='en'):
        self.lang = lang

    def _get_content(self, url):
        print url
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/20.0')
       
        try:
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print "HTTP Error:%s" % (e.reason)
        except Exception, e:
            print "Error occured: %s" % str(e)
        return result

    def search_content(self, query, page=1, limit=10):
        offset = (page - 1) * limit
        url = SEARCH_URL % (self.lang, urllib.quote_plus(query), offset, limit)
        json_str = self._get_content(url).read()
        data = json.loads(json_str)

        search = data['query']['search']
        if not search:
            return

        results = []
        for article in search:
            snippet = article['snippet']
            snippet = re.sub(r'(?m)<.*?>', '', snippet)
            snippet = re.sub(r'\s+', ' ', snippet)
            snippet = snippet.replace('&quot;', '"')
            snippet = snippet.replace(' . ', '. ')
            snippet = snippet.replace(' , ', ', ')
            snippet = snippet.strip()
            
            results.append({
                'title' : article['title'].strip(),
                'snippet' : snippet
            })
        print results
        return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wikipedia search')
    parser.add_argument('--query', action="store", dest="query", required=True)
    given_args = parser.parse_args() 
    wikipedia = Wikipedia()
    search_term = given_args.query
    print "Searching Wikipedia for %s" % search_term 
    results = wikipedia.search_content(search_term)
    print "Listing %s search results..." % len(results)
    
    # Windows 因为终端字符集（字体）问题可能无法打印输出
    for result in results:
        print "==%s== \n \t%s" % (result['title'], result['snippet'])
    print "---- End of search results ----"