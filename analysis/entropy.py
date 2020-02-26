
import re


name = "Character set analysis"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"

success = f"{success} Finished entropy analysis"
fail = f"{fail} Something went wrong on entropy analysis"



def analyse(resultDict, text):
    return False