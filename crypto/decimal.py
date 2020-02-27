
name = "Decimal"
priority=50

## forward check compatibility
def check(result,**kwargs):
    if("charset" in result):
        if(not result["charset"]==r"[0-9 ]"):
            return False
    return True


def decrypt(text, **kwargs):
    text = text.split(' ')
    res = ''
    for c in text:
        res+=chr(int(c))
    return res