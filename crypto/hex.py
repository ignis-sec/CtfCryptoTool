
import binascii
import re
name = "Hex"

def check(results):
    if(results["charset"]==r"[0-9a-fA-F ]" or results["charset"]==r"[0-9 ]"):
        return True
    else:
        return False


def decode(text, key=''):
    text = text.replace(' ', '')
    res = binascii.unhexlify(text).decode()
    #print(res)
    if(re.match(r'^[ -~]*$',res)):
        return res
    else:
        return False