
import binascii
import re
name = "Hex"

def check(results):
    if(results["charset"]==r"[0-9a-fA-F ]"):
        return True
    else:
        return False


def decode(text, key=''):
    text = text.replace(' ', '')
    res = binascii.unhexlify(text).decode()
    #print(res)
    if(re.match(r'^[a-z0-9!"#$%&\'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$',res)):
        return res
    else:
        return False