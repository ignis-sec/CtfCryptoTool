

name = "asci indexes"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

prequisites=["getShift", "plain"]

keys =[3,5,7,9,11,15,17,19,21,23,25]


def analyse(result,text, shared, **kwargs):
    cipherAsciIndex= []
    
    for i in range(len(result["plain"])):
        c = text[i]
        if(not c.isalpha()):
            cipherAsciIndex.append(-1)
        elif(c.islower()):
            cipherAsciIndex.append(shared["getShift"](c, 'a'))
        else:
            cipherAsciIndex.append(shared["getShift"](c, 'A'))
    
    result["cipherAsciIndex"] = cipherAsciIndex

    plainAsciIndex= []
    for c in result["plain"]:
        if(not c.isalpha()):
            plainAsciIndex.append(-1)
        elif(c.islower()):
            plainAsciIndex.append(shared["getShift"](c, 'a'))
        else:
            plainAsciIndex.append(shared["getShift"](c, 'A'))
    
    result["plainAsciIndex"] = plainAsciIndex
    return True