# CtfCryptoTool

This is a tool aiming to significantly cut-off manual-labor of ctf crypto challenges, mostly ones related to classical, non modern ciphers.

Usage:
```
CtfCrpytoTool.py [-h] [-v] [-k KEY] [-b] [-p PLAIN] [-f] [-d DEPTH] [-i IGNORE] ciphertext
```


```
positional arguments:
  ciphertext            ciphertext to analyse

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         set verbosity level
  -k KEY, --key KEY     use a key
  -b, --brute           attempt brute force on the text
  -p PLAIN, --plain PLAIN
                        a part of a plaintext to search for (required for recursive checks)
  -f, --file            give a file instead of cli text
  -d DEPTH, --depth DEPTH
                        depth limit for recursive search
  -i IGNORE, --ignore IGNORE
                        (regex) characters to ignore during charset analysis
```


## Example Usage
### Recursively find solution using flag format
```
python .\CtfCrpytoTool.py "NmIgNzEgNjYgNmMgN2IgNjggNzcgNjQgNzUgNzkgNzQgMjAgNmUgNzggMjAgNmIgN2EgNzMgN2Q=" -p "flag{.*}" -i "[{}]"
```

[![asciicast](https://asciinema.org/a/WBJcaXTLqSRSxD25Ucel7Stwa.svg)](https://asciinema.org/a/WBJcaXTLqSRSxD25Ucel7Stwa)


### Simple Mode
```
python3 CtfCrpytoTool.py "102 108 97 103 123 99 114 121 112 116 111 32 105 115 32 102 117 110 125"
```
[![asciicast](https://asciinema.org/a/zmS7ugLdHOna56xzZb50BqHp6.svg)](https://asciinema.org/a/zmS7ugLdHOna56xzZb50BqHp6)


### Known Key Example (Affine key in the example)

```
python3 CtfCrpytoTool.py "00110001 00110001 00110100 00100000 00110001 00110000 00110110 00100000 00111001 00111001 00100000 00110001 00110001 00110111 00100000 00110001 00110010 00110011 00100000 00110001 00110000 00110101 00100000 00111001 00111000 00100000 00110001 00110001 00111001 00100000 00110001 00110001 00111000 00100000 00110001 00110000 00110100 00100000 00110001 00110001 00110101 00100000 00110011 00110010 00100000 00111001 00110111 00100000 00110001 00110000 00110001 00100000 00110011 00110010 00100000 00110001 00110001 00110100 00100000 00110001 00110000 00110111 00100000 00110001 00110001 00110010 00100000 00110001 00110010 00110101" -p "flag{.*}" -i "[{}]" -k "3,2" -d 3
```
[![asciicast](https://asciinema.org/a/odfZPvsn16nLADGhBI0G8lzAi.svg)](https://asciinema.org/a/odfZPvsn16nLADGhBI0G8lzAi)



# Extending modules

Documentation on how to create a simple module is given below. You can just use one of the templates below, and build on top of that.
To get it imported, just drop it to the correct folder in the tool.

## Analysis modules

Analysis modules are dynamically loaded from the `./analysis` folder.

During the analysis step, tool iterates over all the analysis modules, and calls their analyse function.

---

Very minimal analysis module example:

```py
name = "Ciphertext Length"
success = "Found cipher length"
fail = "failed"

def analyse(result, text, **kwargs):
    result["cipherLength"]=len(text)
    result["cipherLengthNOWS"]=len(text.replace(' ',''))
    return True
```
---

### Analysis module Components:

#### Name:
Name of the module to be printed during the load process

#### Success
Will be printed when analysis is completed in verbose mode

#### Fail
Will be printed if module throws an exception.

---

### Analyse Function
Will be called with following arguements:
```py
module.analyse(results,cipher,ignore=self.ignore, shared=self.sharedData)
```

### Arguements
* results: A dictionary to store all the results for the given ciphertext
* cipher: ciphertext itself
* ignore: characters to ignore during analysis (in regex format, `r"[abc]"`)
* shared: shared data between modules. Data contained in this dictionary is independent from the ciphertext being analysed:
    * example: All the charsets defined in charset analysis module
    * if a crypto module was called before during this run.

--- 




## Crypto Modules

Crypto modules are dynamically loaded from the `./crypto` folder.

After the analysis step, tool iterates over all the crypto modules, and calls their check function.

If check function returns true, then decryption is attempted with decrypt function.

--- 
Very minimal crypto module example:

```py
import binascii
import re
name = "Hex"
priority=50

def check(result,**kwargs):
    if("charset" in result):
        if(not result["charset"]==r"[0-9a-fA-F ]" and not result["charset"]==r"[0-9 ]"):
            return False
    
    if("entropy" in result):
        if(result["entropy"]<=1.95 or result["entropy"]>=4):
            return False
    
    return True


def decrypt(text, **kwargs):
    text = text.replace(' ', '')
    res = binascii.unhexlify(text).decode()
    if(re.match(r'^[ -~]*$',res)):
        return res
    else:
        return False
```

---

### Crypto module Components:

#### Name:
Name of the module to be printed during for the trace output

#### Priority:
Crypto modules are called in order which is sorted on their priority value. Lower priority values algorithms will be called as a last resort.
Default is 50.

---

### Check Function
This is a forward check to see if given ciphertext can be decoded with this module, without actually decoding it.
Returns boolean. True for check-pass, False for check-fail.

It is called with following arguements:
```py
module.check(results,key=self.key,plain=self.plain,text=cipher, shared=self.sharedData)
```

### Arguements
* results: A dictionary to store all the results for the given ciphertext
* key: key to be used if its needed
* plain: Flag format of the plaintext
* cipher: ciphertext
* shared: shared data between modules. Data contained in this dictionary is independent from the ciphertext being analysed:
    * example: All the charsets defined in charset analysis module
    * if a crypto module was called before during this run.

--- 


### Decrypt Function
This function is called if forward checks pass, and attempts to decrypt the ciphertext.

It is called with following arguements:
```py
module.decrypt(cipher,key=self.key,plain=self.plain, shared=self.sharedData)
```

### Arguements

* cipher: ciphertext
* key: key to be used if its needed
* plain: Flag format of the plaintext
* shared: shared data between modules. Data contained in this dictionary is independent from the ciphertext being analysed:
    * example: All the charsets defined in charset analysis module
    * if a crypto module was called before during this run.
