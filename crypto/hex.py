
import binascii
import re
name = "Hex"

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
    res = binascii.unhexlify(text).decode("ansi")
    #print(res)
    if(re.match(r'^[ -~]*$',res)):
        return res
    else:
        return False