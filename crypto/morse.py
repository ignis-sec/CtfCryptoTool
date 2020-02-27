
name="Morse"
priority=40

morse = {
'.-':	    'A',
'-...':	    'B',
'-.-.':	    'C',
'-..':	    'D',
'.':	    'E',
'..-.':	    'F',
'--.':	    'G',
'....':	    'H',
'..':	    'I',
'.---':	    'J',
'-.-':	    'K',
'.-..':	    'L',
'--':	    'M',
'-.':	    'N',
'---':	    'O',
'.--.':	    'P',
'--.-':	    'Q',
'.-.':	    'R',
'...':	    'S',
'-':	    'T',
'..-':	    'U',
'...-':	    'V',
'.--':	    'W',
'-..-':	    'X',
'-.--':	    'Y',
'--..':	    'Z',
'.----':	'1',
'..---':	'2',
'...--':	'3',
'....-':	'4',
'.....':	'5',
'-....':	'6',
'--...':	'7',
'---..':	'8',
'----.':	'9',
'-----':	'0',
'.-.-.-':	'.',
'..--..':	'?',
'-..-.':	'/',
'-....-':	'-',
'-.--.':	'(',
'-.--.-':	')'
}

def check(result,**kwargs):
    if("alphabet" in result):
        if(not len(result["alphabet"])==2 and not len(result["alphabet"])==3):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=1.4 or result["entropy"]>=1.6):
            return False
    return True


def decrypt(text, **kwargs):
    res = ''
    text = text.split(' ')
    for symbol in text:
        if(symbol in morse):
            res+=morse[symbol]
        else:
            res+='?'
    return res