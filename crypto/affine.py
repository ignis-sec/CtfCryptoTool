
import re

name = "Affine"

priority=10
prequisites=["affineKey"]

def egcd(a, b): 
    x,y, u,v = 0,1, 1,0
    while a != 0: 
        q, r = b//a, b%a 
        m, n = x-u*q, y-v*q 
        b,a, x,y, u,v = a,r, u,v, m,n 
    gcd = b 
    return gcd, x, y

def modinv(a, m): 
    gcd, x, y = egcd(a, m) 
    if gcd != 1: 
        return None  # modular inverse does not exist 
    else: 
        return x % m 

## forward check compatibility
def check(result,key,shared,trace,**kwargs):
    if("Affine" in trace):
        return False
    return True


def decrypt(text, key,shared,result, **kwargs):
    key = result["affineKey"]
    key = key.split(",")
    res =''

    for c in text:
        if(not re.match(r"[a-zA-Z]", c)):
            res+=c
            continue
        
        if(c.islower()):
            base=ord('a')
        else:
            base=ord('A')
        res+=chr((( modinv(int(key[0]), 26)*(ord(c) - base - int(key[1]))) % 26) + base)
    
    shared["affineCycleFlag"]=True
    if(re.match(r"[ -~]",res)):
        return res
    else: return False