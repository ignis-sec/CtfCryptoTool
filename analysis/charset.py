
import re


name = "Character set analysis"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Matching charset Found"
fail = f"{fail} Failed to find a matching charset"

charsets = [
    r"[a-z]",           #lowercase
    r"[a-z ]",          #lowercase with space
    r"[a-z \-_]",       #lowercase with space and dashes
    r"[A-Z]",           #uppercase
    r"[A-Z ]",          #uppercase with space
    r"[A-Z \-_]",       #uppercase with space and dashes
    r"[a-zA-Z]",        #characters
    r"[a-zA-Z ]",       #characters with space
    r"[0-9 ]",          #numbers with space
    r"[0-9a-fA-F ]",    #hex
    r"[a-zA-Z0-9]",     #alphanumeric
    r"[a-zA-Z0-9 ]",    #alphanumeric with space
    r"[A-Za-z0-9+/=]",  #b64
    r"[!-u]"#,          #b85
    #r"[0x00-0xff]"     #bytes
]

def analyse(resultDict, text):
    for cset in charsets:
        expr = r"^" + cset + r"+$"
        if(re.match(expr,text)):
            resultDict["charset"] = cset
            return True
    
    resultDict["charset"] = [0x00-0xff]
    return False