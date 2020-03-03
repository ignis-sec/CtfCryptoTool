#Analyse viability of a shift key

name = "Shift Key rot47 variation"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Found a consistent shift"
fail = f"{fail} No consistent shift47 variation found."

prequisites=["plain"]
share=["getShift47"]

def getShift47(c1,c2):
    base=ord('!')
    c1 = ord(c1) - base
    c2 = ord(c2) - base
    return (c1-c2)%94

def analyse(result, text, **kwargs):
    plain = result["plain"]
    key = getShift47(plain[0],text[0])
    for i in range(len(plain)):
        if(getShift47(plain[i],text[i])!=key):
            return False
    result["shiftKey47"] = key
    return True