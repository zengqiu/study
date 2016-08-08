# -*- coding: utf-8 -*-

# 列出 FTP 远程服务器中的文件

import ftplib

FTP_SERVER_URL = 'localhost'

def test_ftp_connection(path, username, email):
    # Open ftp connection
    ftp = ftplib.FTP(path, username, email)
    
    # List the files in the /pub directiory
    ftp.cwd("/pub")
    print "File list at %s:" % path
    files = ftp.dir()
    print files
    ftp.quit()

if __name__ == '__main__':
    test_ftp_connection(path=FTP_SERVER_URL, username='anonymous', email='nobody@nourl.com')