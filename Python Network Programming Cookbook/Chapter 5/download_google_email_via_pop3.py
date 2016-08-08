# -*- coding: utf-8 -*-

# 通过 POP3 协议下载谷歌电子邮件

import argparse
import getpass
import poplib

GOOGLE_POP3_SERVER = 'pop.gmail.com'    # pop.163.com

def download_email(username):
    mailbox = poplib.POP3_SSL(GOOGLE_POP3_SERVER, '995')
    mailbox.user(username)
    password = getpass.getpass(prompt="Enter you Google password: ")
    mailbox.pass_(password)
    num_messages = len(mailbox.list()[1])
    print "Total emails: %s" % num_messages
    print "Getting last message"
    for msg in mailbox.retr(num_messages)[1]:
        print msg
    mailbox.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Email Download Example')
    parser.add_argument('--username', action="store", dest="username", default=getpass.getuser())
    given_args = parser.parse_args()
    username = given_args.username
    download_email(username)