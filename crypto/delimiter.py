
import re

name="swapDelimiter"

# Convert delimiter to standard, whitespace

priority=20

def check(result,text,**kwargs):
    if("cipherLength" in result):
        if(len(re.findall(",",text))>=result["cipherLength"]/5 and len(re.findall(",",text))<=result["cipherLength"]/1.9):
            return True
        if(len(re.findall(", ",text))>=result["cipherLength"]/5 and len(re.findall(",",text))<=result["cipherLength"]/1.9):
            return True
        if(len(re.findall("\t",text))>=result["cipherLength"]/5 and len(re.findall(",",text))<=result["cipherLength"]/1.9):
            return True
        if(len(re.findall("\\\\",text))>=result["cipherLength"]/5 and len(re.findall(",",text))<=result["cipherLength"]/1.9):
            return True
        if(len(re.findall("/",text))>=result["cipherLength"]/5 and len(re.findall(",",text))<=result["cipherLength"]/1.9):
                return True
    return False


def decrypt(text, **kwargs):
    text = re.sub('(,)|(, )|(\t)|(\\\\)|(/)', ' ', text)
    return text