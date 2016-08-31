#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 简单快速的 RSA 公私钥生成脚本

# pip install pycrypto
# 修改 C:\Python27\Lib\site-packages\crypto 为 Crypto（注意大小写）

from Crypto.PublicKey import RSA
new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

print public_key
print private_key