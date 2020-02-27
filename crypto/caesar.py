
name = "caesar"

import re

## forward check compatibility
def check(result,text,plain,shared,**kwargs):
    #check if offset of all the characters is same
    #check if it has extra characters caesar cant use
    if("charsets" in shared):
        if(result["charsetIndex"]>=shared["charsets"].index(r"[a-zA-Z ]")):
            return False
    
    #check if shift is consistent
    offset = ord(plain[0]) - ord(text[0])
    for c in range(3):
        if(offset!=(ord(plain[c]) - ord(text[c]))):
            return False
    return True


def decrypt(text, plain, **kwargs):
    offset = ord(plain[0])-ord(text[0])
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