#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解密数据

import zlib
import base64
from Crypto.PublicKey import RSA 
from Crypto.Cipher import PKCS1_OAEP

encrypted = """bntN8G/8GmtqdY/XNv2P9hwScNJS8QBiAiqqHEEZZ5lDZIt4qR/Q5sQJ0x6kI9pnRZoFwjEYi7yn
kJB85XTQbSsHTYGHXyaSGei0SfjF5dUbbKB71nq9AsiQKmU6v94jmROvY5op9BXgpnfAVrolTi6K
rs4EbflT6fwGs+fB5C+xOmVO4DJRlBS9sKKybbncPW9L8pNmHFiDCg6u6/0GIprjVgPuI/MTH4t2
Oxfs5JLzdCCHT2SqqmL4pV+B7xMB/1kGM6kFiUOd0JkLed7SdDw2HHsWp2BSZR4/xy+iCOGr7rkU
o3cz2IeCmd34R5Gl6aB6kZuNshuSA0PBYmEchg=="""

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2u5E1QysrRsk7/EsnPeDBd3upWYQsH1AiphukaRCdAQ5yTVP
wYaSUjDSGrdv6BVUhzJ0xmlrkOJwNA2MuCJZUQMvjUaMhMZyEDs+oXFZLb6jAJ5X
WFdS31yRwROOfGe7LynfjKFwxgVr2MdiLHgOiErYw4bCvlChUVgOrgs2OiWfc9sw
bNMkgU5Uj2VLqB5v4Ck+cFaYSCExPSytpHsWm7uGuLdAB748TJDFRxs/Ush/yvfp
xZPIfdfLXk1CZn0uynfLskKXkl0Gr8sU+uuZ6DKPWrv/lAL6fqm9L4uxPofaWqlr
3uHERy1xgVUyCdB3kN/QgiVSWDja3TKj58hBEwIDAQABAoIBAFRSlVxhp1h9Lfrk
r0Q96M8nrbUy3Ja9h1Baaava0mWRAxjGWdO2G0Fg4Gu933JKVOZFvsh07iM9s+24
kkyRnkkfqv8E/zZcoK4zw2m3GJwP4wRn+EhkSd0R8GmnOKgd4/DEdf/aZm8+w00Z
bmymSSKhgV+91eAreha0jeLnGpnGEYDmtECD13x+0cwWyTngyqL3SqZGynPDUPUl
/YT0a/1B+u+Aq5Ilo7qQB2JxY8hvMm76PinnhDo14BomAeUfzjaBt+3OAvJeo6N/
g90CJq1eQaHBm3bO3km0mRq096dsN4sC3NhV5xYxDBO1BrCmRpamdILMeX6Y0DMw
C216F7ECgYEA6JrqnJQZOPJhCOOx3kfqHI+y6W2ezx3tTp3TuazeAEjJ3zzXhqql
DkWFvgYV2Q6PfBgsFnHscTDnm7iccqmZ4PMaMy7osmPDjbUoz5I0976KA7nA02OK
ObgePxiOyvY5OnwiwwPa+8Q5+U4H1g3ZxvAIRrK9KmtkIM/jbblrRucCgYEA8PNE
Daho3d0JQ4cab0Fksl2wGpPp+v8FaHg178d7KdHhHwAbaHGiKBUU8pSFYxVwTIPV
KijbwK1I18IGnGNwpbT3GRiUHzrgFHOszgjP6PpTv+ZRgfwoInniTGGxHbvnrNac
fHuqW0NHgIJQ7Np3LKIWxV7c92+yrsY2dZe4qvUCgYEAnKmaUpM82aoFyOLyrW9q
MopmSenXCFBzwHt0Wp4fd7mOnZhw4PaV7KLOjUmz9VllMoNlTki0oxf5JlyUonWw
el3By69QcrXWw967+fHTUvk2I4Q8ZyOnuXBUjtKPeguUR9vL3eT+3IsxMMRparYx
c1e/ez5vQd7KtX7PAtvbcQkCgYEApqHl33gnRcAWJwApFOXpiLzoDAldGDsDd3Mj
Afc3wv0lrfW5/qoPVZ72xKhX8uUhq5jEc4qcJwzvwl6pib/vaHnVJSLtVQe3bg1t
ZXOMrXdpMd5LYhSLgQQ/r0kkXwbTOqGUyTYQ41qM+V+mLZcMMe7KxqZLNEeoD9x+
TyalDH0CgYA45CmvxYefnkg5C1dDZUmhszxd9DmWdTwyE/5J3ZfRt9k3hlr+8Z+b
tqzwj3XzMOVy3n5OBP7pUNtQSFqP1FhXpQ6KCgdScR6//BWNPm4j60S5GqgRXldp
vl+ko4AS7f2G1lCHL7LEeRRQFgynepnHzrQMz9uMd7Dp9535q+JqFw==
-----END RSA PRIVATE KEY-----"""

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset+256])
    offset += 256

# Now we decompress to original
plaintext = zlib.decompress(decrypted)

print plaintext