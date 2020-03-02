

import re

name = "rot47"
priority=25
prequisites=["shiftKey47"]

## forward check compatibility
def check(result,text,plain,shared,**kwargs):
    return True


def decrypt(text, plain,result, **kwargs):
    offset = ord(plain[0])-ord(text[0])
    res = ''
    key = result["shiftKey47"]
    for c in text:
        if(c==' '):
            res+=c
            continue
        base=ord('!')
        res += chr(base + (ord(c)-base+key)%94)
    return res