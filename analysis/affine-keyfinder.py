
import re

#Known plaintext attack on affine

name = "Affine Keyfinder PT"

fail="[\033[91m+\033[0m] No affine keys found"
success="[\033[92m+\033[0m] Found Affine Key"

prequisites=["getShift", "plain", "cipherAsciIndex", "plainAsciIndex"]

keys =[3,5,7,9,11,15,17,19,21,23,25]


def analyse(result,text, shared, **kwargs):
    plain = result["plain"]
    if("key" in result):
        key = result["key"]
        if(re.match(r"^\d+,\d+$", key)):
            result["affineKey"] = key
            return True
    
    cipher = result["cipherAsciIndex"]
    plain = result["plainAsciIndex"]

    for key in keys:
        cura=key
        curb=(cura*plain[0]-cipher[0])%26
        bKeyFailed=False
        for i in range(len(plain)):
            
            p = plain[i]
            c = cipher[i]
            #print(f"index: {p} {c}")
            a = key
            b = (a*p-c)%26
            if(c==-1 or p==-1):
                continue
            if(b!=curb):
                bKeyFailed=True
                break
            #print(f"{a} {b}") 
        if(not bKeyFailed):
            #print(f"Affine key found with {cura},{curb}")
            result["affineKey"] = f"{cura},{26-curb}"
            return True



    return False