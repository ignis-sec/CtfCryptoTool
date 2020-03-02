name = "Alphabet Analysis"

fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m] Completed Alphabet Analysis"

def analyse(result, text, **kwargs):
    alphabet = list(set(text))
    result["alphabet"]=alphabet
    return True