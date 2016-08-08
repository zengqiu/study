# -*- coding: utf-8 -*-

# 提交网页表单

import requests
import urllib
import urllib2
from lxml import html

ID_NAME = 'name'
ID_EMAIL = 'email'
ID_PASSWORD = 'password'
ID_CONFIRM = 'confirm'
ID_GPG_KEYID = 'gpg_keyid'
NAME = 'fortestzz3'
EMAIL = 'fortestzz3@163.com'
PASSWORD = 'fortestzz3fortestzz3'
CONFIRM = 'fortestzz3fortestzz3'
GPG_KEYID = ''

SIGNUP_URL = 'https://pypi.python.org/pypi'

def submit_form():
    """Submit a form"""
    payload = {
        ID_NAME: NAME,
        ID_EMAIL: EMAIL,
        ID_PASSWORD: PASSWORD,
        ID_CONFIRM: CONFIRM,
        ID_GPG_KEYID: GPG_KEYID,
        ':action': 'user'
    }
    
    # Make a GET request
    resp = requests.get(SIGNUP_URL)
    print "Response to GET request: %s" % resp.content

    # Send POST request
    resp = requests.post(SIGNUP_URL, payload)
    print resp.status_code
    print "Headers from a POST request response: %s" % resp.headers
    # print "HTML Response: %s" % resp.text
    
def submit_form_prefect():
    ses = requests.session()
    r = ses.get(SIGNUP_URL)
    cookies = r.cookies

    # 可以采用如下方式获取 token（如果 post 需要 token）
    # tree = html.fromstring(resp.text)
    # token = list(set(tree.xpath("//input[@name='token']/@value")))[0]
    
    payload = {
        ID_NAME: NAME,
        ID_EMAIL: EMAIL,
        ID_PASSWORD: PASSWORD,
        ID_CONFIRM: CONFIRM,
        ID_GPG_KEYID: GPG_KEYID,
        ':action': 'user'
    }
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Length': '127',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Host': 'pypi.python.org',
        'Referer': 'https://pypi.python.org/pypi?:action=register_form',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }

    # Send POST request
    resp = ses.post(SIGNUP_URL, data=payload, headers=headers, cookies=cookies)
    print resp.status_code
    print "Headers from a POST request response: %s" % resp.headers

if __name__ == '__main__':
    submit_form()