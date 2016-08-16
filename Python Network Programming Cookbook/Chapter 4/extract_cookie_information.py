# -*- coding: utf-8 -*-

# 访问网站后提取 cookie 信息

import cookielib
import urllib
import urllib2

ID_USERNAME = 'username'
ID_PASSWORD = 'password'
USERNAME = ''
PASSWORD = ''
LOGIN_URL = 'https://bitbucket.org/account/signin/?next=/'
NORMAL_URL = 'https://bitbucket.org/'

def extract_cookie_info():
    """Fake login to a site with cookie"""
    # Setup cookie jar
    cj = cookielib.CookieJar()
    
    # Create url opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.open(LOGIN_URL)

    try:
        token = [cookie.value for cookie in cj if cookie.name == 'csrftoken'][0]
    except IndexError:
        return False, "No csrftoken"
    
    login_data = urllib.urlencode({'csrfmiddlewaretoken': token, ID_USERNAME: USERNAME, ID_PASSWORD: PASSWORD, 'this_is_the_login_form': True})
    
    resp = opener.open(LOGIN_URL, login_data)

    # Send login info
    for cookie in cj:
        print '----First time cookie: %s --> %s' % (cookie.name, cookie.value)

    print "Headers: %s" % resp.headers

    # Now access without any login info
    resp = opener.open(NORMAL_URL)
    for cookie in cj:
        print "++++Second time cookie: %s --> %s" % (cookie.name, cookie.value)

    print "Headers: %s" % resp.headers

if __name__ == '__main__':
    extract_cookie_info()