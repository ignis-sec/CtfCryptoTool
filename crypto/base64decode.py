
import base64
import re
name = "Base64"
priority=50

def check(result,**kwargs):
    if("charset" in result):
        if(not result["charset"]==r"[A-Za-z0-9+/=]" and not result["charset"]==r"[a-zA-Z0-9]"):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=2.0 or result["entropy"]>=5):
            return False
    
    return True


def decrypt(text, **kwargs):
    res = base64.b64decode(text).decode()
    print(res)
    if(re.match(r'^[ -~]*$',res)):
        return res
    else:
        return False