
import base64
import re

name = "Binary"
priority=50
## forward check compatibility
def check(result,**kwargs):
    if("alphabet" in result):
        if(not len(result["alphabet"])==2 and not len(result["alphabet"])==3):
            return False
    
    if("cipherLengthNOWS" in result):
        if(result["cipherLengthNOWS"]%8):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=1.28 or result["entropy"]>=1.39):
            return False
    return True


def decrypt(text, **kwargs):
    text = text.replace(' ', '')
    binaryStream = int(text,2)
    res = binaryStream.to_bytes((binaryStream.bit_length() + 7) // 8, 'big')
    return res.decode()