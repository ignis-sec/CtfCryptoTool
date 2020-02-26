
import base64
import re
name = "Base64"

def check(results):
    if(results["charset"]==r"[A-Za-z0-9+/=]"):
        return True
    else:
        return False


def decode(text):
    #print(text)
    res = base64.b64decode(text).decode()
    print(res)
    if(re.match(r'^[a-z0-9!"#$%&\'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$',res)):
        return res
    else:
        return False