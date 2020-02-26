
import base64
import re

name = "Binary"

## forward check compatibility
def check(result):
    if("alphabet" in result):
        if(not len(result["alphabet"])==2 and not len(result["alphabet"])==3):
            return False
    
    if("cipherLengthNOWS" in result):
        if(result["cipherLengthNOWS"]%8):
            return False
    return True


def decrypt(text, **kwargs):
    text = text.replace(' ', '')
    binaryStream = int(text,2)
    res = binaryStream.to_bytes((binaryStream.bit_length() + 7) // 8, 'big')
    return res.decode()