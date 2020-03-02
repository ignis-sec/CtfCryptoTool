
import math

#Run shannon entropy analysis on the text

name = "Frequency Analysis"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Finished frequency analysis"
fail = f"{fail} Something went wrong with frequency analysis"

prequisites=["alphabet"]

def analyse(result, text, **kwargs):
    freqList = []
    text = list(text)
    ent = 0
    alphabet = result["alphabet"]
    for symbol in alphabet:
        ctr = 0
        for sym in text:
            if sym == symbol:
                ctr += 1
        freqList.append(float(ctr) / len(text))
    result["frequency"]=freqList
    return True