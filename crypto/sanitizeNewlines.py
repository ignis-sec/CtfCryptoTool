
name = "sanitizeNewlines"
priority=0

import re

## forward check compatibility
def check(result,text,plain,shared,**kwargs):
    if("\n" in text):
        return True
    return False


def decrypt(text, plain, **kwargs):
    return text.replace('\n', '')