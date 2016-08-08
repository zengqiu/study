# -*- coding: utf-8 -*-

# 编写一个支持断点续传功能的 HTTP 容错客户端

import urllib
import os

TARGET_URL = 'http://www.embeddedsystem.org/crosstool/5.2.0/'
TARGET_FILE = 'crosstool-5.2.0.tar.bz2'

class CustomURLOpener(urllib.FancyURLopener):
    """Override FancyURLopener to skip error 206 (when a partial file is being sent)"""
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass

def resume_download():
    file_exists = False
    CustomURLClass = CustomURLOpener()
    if os.path.exists(TARGET_FILE):
        out_file = open(TARGET_FILE, 'ab')
        file_exists = os.path.getsize(TARGET_FILE)
        # If the file exists, then only download the unfinished part
        CustomURLClass.addheader("range", "bytes=%s-" % (file_exists))
    else:
        out_file = open(TARGET_FILE, 'wb')

    web_page = CustomURLClass.open(TARGET_URL + TARGET_FILE)

    # Check if last download was OK
    if int(web_page.headers['Content-Length']) == file_exists:
        loop = 0
        print "File already downloaded!"

    byte_count = 0
    while True:
        data = web_page.read(8192)
        if not data:
            break
        out_file.write(data)
        byte_count = byte_count + len(data)

    web_page.close()
    out_file.close()

    for k, v in web_page.headers.items():
        print k, '=', v
    print "File copied", byte_count, "bytes from", web_page.url

if __name__ == '__main__':
    resume_download()