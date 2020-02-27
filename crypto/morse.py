
name="Morse"
priority=40

morse = {
  "-----": "0",
  ".----": "1",
  "..---": "2",
  "...--": "3",
  "....-": "4",
  ".....": "5",
  "-....": "6",
  "--...": "7",
  "---..": "8",
  "----.": "9",
  ".-": "a",
  "-...": "b",
  "-.-.": "c",
  "-..": "d",
  ".": "e",
  "..-.": "f",
  "--.": "g",
  "....": "h",
  "..": "i",
  ".---": "j",
  "-.-": "k",
  ".-..": "l",
  "--": "m",
  "-.": "n",
  "---": "o",
  ".--.": "p",
  "--.-": "q",
  ".-.": "r",
  "...": "s",
  "-": "t",
  "..-": "u",
  "...-": "v",
  ".--": "w",
  "-..-": "x",
  "-.--": "y",
  "--..": "z",
  ".-.-.-": ".",
  "--..--": ",",
  "..--..": "?",
  "-.-.--": "!",
  "-....-": "-",
  "-..-.": "/",
  ".--.-.": "@",
  "-.--.": "(",
  ")": "-.--.-"
}

def check(result,**kwargs):
    if("alphabet" in result):
        if(not len(result["alphabet"])==2 and not len(result["alphabet"])==3):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=1.2 or result["entropy"]>=1.6):
            return False
    return True


def decrypt(text, **kwargs):
    res = ''
    text = text.split(' ')
    for symbol in text:
        if(symbol in morse):
            res+=morse[symbol]
        else:
            pass
            #res+='?'
    return res