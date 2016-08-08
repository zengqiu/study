# -*- coding: utf-8 -*-

# 把本地文件上传到远程 FTP 服务器中

import os
import argparse
import getpass
import ftplib

LOCAL_FTP_SERVER = 'localhost'
LOCAL_FILE = 'readme.txt'
FTP_USER = 'zengqiu'    # getpass.getuser()

def ftp_upload(ftp_server, username, password, file_name):
    print "Connecting to FTP server: %s" % ftp_server
    ftp = ftplib.FTP(ftp_server)
    print "Login to FTP server: user=%s" % username
    ftp.login(username, password)
    ext = os.path.splitext(file_name)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file_name, open(file_name))
    else:
        ftp.storbinary("STOR " + file_name, open(file_name, "rb"), 1024)
    print "Uploaded file: %s" % file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FTP Server Upload Example')
    parser.add_argument('--ftp-server', action="store", dest="ftp_server", default=LOCAL_FTP_SERVER)
    parser.add_argument('--file-name', action="store", dest="file_name", default=LOCAL_FILE)
    parser.add_argument('--username', action="store", dest="username", default=FTP_USER)
    given_args = parser.parse_args() 
    ftp_server, file_name, username = given_args.ftp_server, given_args.file_name, given_args.username
    password = getpass.getpass(prompt="Enter you FTP password: ") 
    ftp_upload(ftp_server, username, password, file_name)