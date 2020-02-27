
import re


name = "Character set analysis"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Matching charset Found"
fail = f"{fail} Failed to find a matching charset"

charsets = [
    r"[a-z]",           #0lowercase
    r"[a-z ]",          #1lowercase with space
    r"[a-z \-_]",       #2lowercase with space and dashes
    r"[A-Z]",           #3uppercase
    r"[A-Z ]",          #4uppercase with space
    r"[A-Z \-_]",       #5uppercase with space and dashes
    r"[a-zA-Z]",        #6characters
    r"[a-zA-Z ]",       #7characters with space
    r"[0-9 ]",          #8numbers with space
    r"[0-9a-fA-F ]",    #9hex
    r"[a-zA-Z0-9]",     #10alphanumeric
    r"[a-zA-Z0-9 ]",    #11alphanumeric with space
    r"[A-Za-z0-9+/=]",  #12b64
    r"[!-u]",           #13b85
    r"[ -~]"            #14all printables
]

def analyse(result, text, ignore,**kwargs):
    text = re.sub(ignore, '', text)
    counter=0
    for cset in charsets:
        expr = r"^" + cset + r"+$"
        if(re.match(expr,text)):
            result["charset"] = cset
            result["charsetIndex"] = counter
            return True
        counter+=1
    
    result["charset"] = [0x00-0xff]
    result["charsetIndex"] = 99
    return False