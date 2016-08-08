# -*- coding: utf-8 -*-

# 通过 POP3 协议下载谷歌电子邮件

import argparse
import getpass
import imaplib

# Gmail 需要关闭两步验证 https://myaccount.google.com/security/signinoptions/two-step-verification
# Gmail 需要运行低安全的应用访问 https://www.google.com/settings/security/lesssecureapps
# 163 需要允许其他客户端连接 http://config.mail.163.com/settings/imap/index.jsp?uid=YOUR_EMAIL_ADDRESS

GOOGLE_IMAP_SERVER = 'imap.gmail.com'    # imap.163.com

def check_email(username): 
    mailbox = imaplib.IMAP4_SSL(GOOGLE_IMAP_SERVER, '993') 
    password = getpass.getpass(prompt="Enter your Google password: ")
    mailbox.login(username, password)
    # print mailbox.list()
    mailbox.select('Inbox')
    typ, data = mailbox.search(None, 'ALL')
    for num in data[0].split():
        typ, data = mailbox.fetch(num, '(RFC822)')
        print 'Message %s\n%s\n' % (num, data[0][1])
        break
    mailbox.close()
    mailbox.logout()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Email Download Example')
    parser.add_argument('--username', action="store", dest="username", default=getpass.getuser())
    given_args = parser.parse_args() 
    username = given_args.username
    check_email(username)