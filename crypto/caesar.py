
name = "caesar"

import re


## forward check compatibility
def check(result,**kwargs):
    #if("charset" in result):
    #    if(not result["charset"]==r"[a-z]" and not result["charset"]==r"[a-z ]" and not result["charset"]==r"[A-Z ]" and not result["charset"]==r"[A-Z]"):
    #        return False
    return True


def decrypt(text, plain, **kwargs):

    offset = ord(text[0])-ord(plain[0])
    res = ''
    for c in text:
        if(c.islower()):
            base=ord('a')
        else:
            base=ord('A')
        if(not re.match(r"[a-zA-Z]", c)):
            res+=c
            continue
        res += chr(base + (ord(c)-base + offset)%26)

    return res