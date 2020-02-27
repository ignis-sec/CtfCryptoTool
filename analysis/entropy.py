
import math



name = "Shannon Entropy"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Finished entropy analysis"
fail = f"{fail} Something went wrong on entropy analysis"



def analyse(result, text, **kwargs):
    freqList = []
    text = list(text)
    alphabet = list(set(text))
    ent = 0
    for symbol in alphabet:
        ctr = 0
        for sym in text:
            if sym == symbol:
                ctr += 1
        freqList.append(float(ctr) / len(text))
    for freq in freqList:
        ent = ent + freq * math.log(freq, 2)
    ent = ent*-1
    result["alphabet"]=alphabet
    result["entropy"] = ent
    return True