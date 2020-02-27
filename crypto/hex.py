
import binascii
import re
name = "Hex"
priority=50

def check(result,**kwargs):
    if("charset" in result):
        if(not result["charset"]==r"[0-9a-fA-F ]" and not result["charset"]==r"[0-9 ]"):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=1.95 or result["entropy"]>=4):
            return False
    
    return True


def decrypt(text, **kwargs):
    text = text.replace(' ', '')
    res = binascii.unhexlify(text).decode()
    #print(res)
    if(re.match(r'^[\t-~]*$',res)):
        return res
    else:
        return False