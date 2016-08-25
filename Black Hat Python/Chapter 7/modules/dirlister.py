#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 列举当前目录下的所有文件

import os

def run(**args):
    print "[*] In dirlister module."
    files = os.listdir(".")
    
    return str(files)