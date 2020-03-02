
import math

#Run shannon entropy analysis on the text

name = "Shannon Entropy"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Finished entropy analysis"
fail = f"{fail} Something went wrong on entropy analysis"

prequisites=["frequency","alphabet"]

def analyse(result, text, **kwargs):
    ent = 0
    alphabet = result["alphabet"]
    freqList = result["frequency"]
    for freq in freqList:
        ent = ent + freq * math.log(freq, 2)
    ent = ent*-1
    result["entropy"] = ent
    return True