#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Used for compiling bhp_net

from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = ['bhp_net.py'],
    zipfile = None,
)