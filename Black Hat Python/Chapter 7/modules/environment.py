#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 获取机器环境变量

import os

def run(**args):
    print "[*] In environment module."
    return str(os.environ)