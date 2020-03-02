
import base64
import re
name = "Base85ipv6"
priority=50

prequisite=["charset"]
def check(result,**kwargs):
    if(not result["charset"]==r"[!-u]"):
        return False
    
    if("entropy" in result):
        if(result["entropy"]<3.5):
            return False
    
    return True


def decrypt(text, **kwargs):
    res = base64.b85decode(text.encode()).decode()
    return res
