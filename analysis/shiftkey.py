#Analyse viability of a shift key

name = "Shift Key"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Found a consistent shift"
fail = f"{fail} No consistent shift found."

prequisites=["plain"]

def getShift(c1,c2):
    if(not c1.isalpha() or not c2.isalpha()):
        return -1
    if(c1.islower()):
        base = ord('a')
    else:
        base = ord('A')
    c1 = ord(c1) - base
    c2 = ord(c2) - base
    return (c1-c2)%26

def analyse(result, text, **kwargs):
    plain = result["plain"]
    key = getShift(plain[0],text[0])
    for i in range(len(plain)):
        if(getShift(plain[i],text[i])!=key):
            return False
    if(key==-1):
        return False
    result["shiftKey"] = key
    return True