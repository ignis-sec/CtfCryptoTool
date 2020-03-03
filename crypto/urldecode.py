
name = "urlDecode"
priority=100

import binascii
import re

## forward check compatibility
def check(result,text,plain,shared,**kwargs):
    if(re.search("\\%[0-9a-fA-F]{2}",text)):
        return True


def decrypt(text, **kwargs):
    res = text
    found = re.findall("%[0-9a-fA-F]{2}",text)
    for sym in found:
        res = res.replace(sym,binascii.unhexlify(sym[1::]).decode())
    return res