# -*- coding: utf-8 -*-

# 搜索 GitHub 中的源代码仓库

import argparse
import requests
import json

SEARCH_URL_BASE = 'https://api.github.com/repos'

def search_repository(author, repo, search_for='homepage'):
    url = "%s/%s/%s" % (SEARCH_URL_BASE, author, repo)
    print "Searching Repo URL: %s" % url
    result = requests.get(url)
    if result.ok:
        repo_info = json.loads(result.text or result.content)
        # print repo_info
        print "Github repository info for: %s" % repo
        result = "No result found!"
        keys = [] 
        for key, value in repo_info.iteritems():
            if search_for in key:
                result = value
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github search')
    parser.add_argument('--author', action="store", dest="author", required=True)
    parser.add_argument('--repo', action="store", dest="repo", required=True)
    parser.add_argument('--search_for', action="store", dest="search_for", required=True)
    
    given_args = parser.parse_args() 
    result = search_repository(given_args.author, given_args.repo, given_args.search_for)
    if isinstance(result, dict):
        print "Got result for '%s'..." % (given_args.search_for)
        for key, value in result.iteritems():
            print "%s => %s" % (key, value)
    else:
        print "Got result for %s: %s" % (given_args.search_for, result)