import argparse

from internals import *

#configure arguement parser
parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose", action="count", help="set verbosity level")
parser.add_argument("-k","--key", action="store_true", help="use a key")
parser.add_argument("-b","--brute", action="store_true", help="attempt brute force on the text")
parser.add_argument("-p","--plain", help="a part of a plaintext to search for (required for recursive checks)")
parser.add_argument("-f","--file", action="store_true",help="give a file instead of cli text")
parser.add_argument("ciphertext", help="ciphertext to analyse")

#set from parser
args = parser.parse_args() 

if(args.file):
    ciphertext = open(args.ciphertext,"r").read()
else:
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
info="[\033[94m+\033[0m]"


#get all module files from ./analysis and ./crypto
selfdir = os.path.dirname(os.path.realpath(__file__))

#Initialize module lists for dynamic loader
anModuleFolder = os.path.join(selfdir, "analysis")
crModuleFolder = os.path.join(selfdir, "crypto")


analyser = CryptoAnalyser(args.verbose, anModuleFolder, crModuleFolder,'',args.plain)


if(verbosity): print(f"{info} Importing analysis modules...")
analyser.loadAnalysisModules()


if(verbosity): print(f"{info} Importing crypto modules...")
analyser.loadCryptoModules()


#start analysis
analyser.analyseCipher(ciphertext)