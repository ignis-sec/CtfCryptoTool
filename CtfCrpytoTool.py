import argparse
import os
import importlib.machinery
import re

#configure arguement parser
parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose", action="count", help="set verbosity level")
parser.add_argument("-k","--key", action="store_true", help="use a key")
parser.add_argument("-b","--brute", action="store_true", help="attempt brute force on the text")
parser.add_argument("-p","--plain", help="a part of a plaintext to search for (required for recursive checks)")
parser.add_argument("ciphertext", help="ciphertext to analyse")

#set from parser
args = parser.parse_args() 
ciphertext = args.ciphertext
bKey = args.key
plainMode = False
if(args.plain):
    plainMode = True
    plain = args.plain
try:
    verbosity = int(args.verbose)
except:
    verbosity=0


#pretty output headers
fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"
warn="[\033[93m+\033[0m]"
info="[\033[94m+\033[0m]"

#get all module files from ./analysis and ./crypto
selfdir = os.path.dirname(os.path.realpath(__file__))
anModuleFolder = os.path.join(selfdir, "analysis")
crModuleFolder = os.path.join(selfdir, "crypto")

#Initialize module lists for dynamic loader

anModuleFiles = os.listdir(anModuleFolder)
crModuleFiles = os.listdir(crModuleFolder)
anModules = []
crModules = []


if(verbosity): print(f"{info} Importing analysis modules...")
#Dynamically load analysis module files
for moduleFile in anModuleFiles:
    #ignore non .py files
    if not moduleFile.endswith(".py"):
        continue

    #strip file extension
    moduleName = moduleFile.replace('.py', '')
    try:
        #import module from the module folder
        module = importlib.machinery.SourceFileLoader(moduleName, os.path.join(anModuleFolder, moduleFile)).load_module()
        if(verbosity): print(f'\t{success} Imported module: "{module.name}"')
        
        #add it to the list to iterate later
        anModules.append(module)
    except:
        print(f"\t{fail} Failed to import analysis module at {moduleFile}")

if(verbosity): print(f"{info} Importing crypto modules...")
#Dynamically load analysis module files
for moduleFile in crModuleFiles:
    #ignore non .py files
    if not moduleFile.endswith(".py"):
        continue

    #strip file extension
    moduleName = moduleFile.replace('.py', '')
    try:
        #import module from the module folder
        module = importlib.machinery.SourceFileLoader(moduleName, os.path.join(crModuleFolder, moduleFile)).load_module()
        if(verbosity): print(f'\t{success} Imported module: "{module.name}"')
        
        #add it to the list to iterate later
        crModules.append(module)
    except:
        print(f"\t{fail} Failed to import analysis module at {moduleFile}")



def analyseCipher(cipher):
    results = {}
    ### iterate and call each module
    print(f"{warn} Starting the analysis step.")
    for module in anModules:
        res = module.analyse(results,cipher)
        if(res):
            if(verbosity>=2): print(module.success)
        else:
            if(verbosity): print(module.fail)

    print(f"{warn} Analysis results:")
    print(results)

    findDecipher(results, cipher)


def findDecipher(results, cipher):
    for module in crModules:
        if(not module.check(results)):
            if(verbosity>=2): print(f"{warn} Failed primary check for {module.name}")
            continue
    
        try:
            res = module.decode(cipher)
            if(not res):
                if(verbosity>=2): print(f"{warn} Failed secondary check for {module.name}")
            else:
                print("#######################################################")
                print("#####################POSSIBLE RESULT###################")
                print("#######################################################")
                print(f"{success} {module.name} returned: {res}")
                if(plainMode):
                    if(re.match(plain,res)):
                        print(f"{success} Expected plaintext found. Stopping")
                        return
                    else:
                        print(f"{warn} Missing expected plaintext. Continuing.")
                        analyseCipher(res)
        except Exception as e:
            print(e)
            if(verbosity): print(f"{fail} Failed to use {module.name}")



analyseCipher(ciphertext)