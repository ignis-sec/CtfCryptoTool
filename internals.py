import os
import importlib.machinery
import re

#pretty output headers
fail="[\033[91m+\033[0m]"
success="[\033[92m+\033[0m]"
warn="[\033[93m+\033[0m]"
info="[\033[94m+\033[0m]"
warn_start = "\033[93m"
success_start = "\033[92m"
reset = "\033[0m"


class CryptoAnalyser():
    ''' Analysis class for CtfCryptoTool.
    '''
    def __init__(self,verbosity, analysisFolder, cryptoFolder, depth=10, key='',plain='',ignore=''):
        if(verbosity):
            self.verbosity=verbosity
        else:
            self.verbosity=0
        if(plain):
            self.plainMode=True
        else:
            self.plainMode=False
        self.plain=plain
        self.anModules=[]
        self.crModules=[]
        self.anModuleFolder = analysisFolder
        self.crModuleFolder = cryptoFolder
        self.key = key
        self.resultFound=False
        self.depth=depth
        self.counter=0
        self.ignore=ignore
                
        #shared data is used for passing data not related to the cipher to other modules. 
        #Modules should not update the shared data for every round, they should initialize it once.
        self.sharedData = {}


    def analyseCipher(self,cipher, depth, trace='cipher'):
        ''' Iterate over analysis modules on the ciphertext, then call the findDecipher function.
            
            cipher: ciphertext to analyse

            depth: current depth, will be cutoff at self.depth

            trace: used decryption methods so far on the stack

            Every result from the analysis modules should be added to the results dictionary.
            
        '''
        if(self.resultFound):
            return
        # all the analysis results will be stored in this dictionary. All the decrypt forward-checks will check from this dictionary
        results = {}
        results["key"]=self.key
        results["plain"]=self.plain
        
        #cutoff
        if(depth==self.depth):
            print(f"{fail} Depth limit reached.")
            return

        ### iterate and call each modules analysis function
        print(f"{warn} Starting the analysis step.")
        for module in self.anModules:
            res = module.analyse(results,cipher,ignore=self.ignore, shared=self.sharedData)
            if(res):
                if(self.verbosity>=2): print(module.success)
            else:
                if(self.verbosity): print(module.fail)

        print(f"{warn} Analysis results:")
        print(results)

        # attempt decryption now that analysis is complete
        self.findDecipher(results, cipher,trace,depth)


    def findDecipher(self,results, cipher,trace,depth):
        ''' Iterate over crypto modules, and call their check function first. If check returns true, attempt decryption.
            
            results: result dictionary
            
            cipher: ciphertext

            trace: used decryption methods so far on the stack

            depth: current depth, will be cutoff at self.depth
        '''

        #iteration counter, for performance checking
        self.counter+=1

        #if result is already found, don't traverse decryption tree further.
        if(self.resultFound):
            return

        #iterate each module
        for module in self.crModules:
            if(self.resultFound):
                return
            #forward check for each encryption depending on our analysis. Don't bother if it doesn't pass the forward checks. 
            if(not module.check(results,key=self.key,plain=self.plain,text=cipher, shared=self.sharedData)):
                if(self.verbosity>=2): print(f"{warn} Failed primary check for {module.name}")
                continue
        
            #if forward check passes, attempt to decode with the module
            try:
                res = module.decrypt(cipher,key=self.key,plain=self.plain, shared=self.sharedData)
                # module should return false if it successfully decrypts, but result looks like nonsense.
                if(not res):
                    if(self.verbosity>=2): print(f"{warn} Failed secondary check for {module.name}")
                else:
                    if(self.plainMode):
                        #passed all the checks, but still not the plaintext we were expecting
                        if(re.match(self.plain,res)):
                            #Matching expected flag format, finalise
                            print(f"{success_start}#######################################################{reset}")
                            print(f"{success_start}#####################POSSIBLE RESULT###################{reset}")
                            print(f"{success_start}#######################################################{reset}")
                            print(f"{success} {module.name} returned: {res}")
                            print(f"{success} Expected plaintext found. Stopping")
                            print(f"{success} trace: {trace}-->{module.name}-->plain")
                            print(f"{info} total iterations:{self.counter}")
                            self.resultFound=True
                            return
                        else:
                            #looks like a successfull decryption, but not matching the flag format. Output, but continue.
                            #It might be an intermediate step, or flag without proper formatting.
                            if(self.verbosity):
                                print(f"{warn_start}#######################################################{reset}")
                                print(f"{warn_start}#####################POSSIBLE RESULT###################{reset}")
                                print(f"{warn_start}#######################################################{reset}")
                            print(f"{success} {module.name} returned: {res}")
                            print(f"{warn} Missing expected plaintext. Continuing.")
                            self.analyseCipher(res,depth+1,trace+"-->" + module.name)
                    else:
                        #no plain given
                        print(f"{success} {module.name} returned: {res}")
            #most likely module.decrypt failed
            except Exception as e:
                print(e)
                if(self.verbosity): print(f"{fail} Failed to use {module.name}")
        if(not self.resultFound): 
            print(f"{info} Out of ideas ¯\\_(ツ)_/¯")

    #dynamic load from analysis folder
    def loadAnalysisModules(self):
        self.anModuleFiles = os.listdir(self.anModuleFolder)
        for moduleFile in self.anModuleFiles:
            #ignore non .py files
            if not moduleFile.endswith(".py"):
                continue

            #strip file extension
            moduleName = moduleFile.replace('.py', '')
            try:
                #import module from the module folder
                module = importlib.machinery.SourceFileLoader(moduleName, os.path.join(self.anModuleFolder, moduleFile)).load_module()
                if(self.verbosity): print(f'\t{success} Imported module: "{module.name}"')
                
                #add it to the list to iterate later
                self.anModules.append(module)
            except Exception as e:
                print(f"\t{fail} Failed to import analysis module at {moduleFile}")
                print(e)
        
        
    #dynamic load from crypto folder
    def loadCryptoModules(self):
        self.crModuleFiles = os.listdir(self.crModuleFolder)
        for moduleFile in self.crModuleFiles:
            #ignore non .py files
            if not moduleFile.endswith(".py"):
                continue

            #strip file extension
            moduleName = moduleFile.replace('.py', '')
            try:
                #import module from the module folder
                module = importlib.machinery.SourceFileLoader(moduleName, os.path.join(self.crModuleFolder, moduleFile)).load_module()
                if(self.verbosity): print(f'\t{success} Imported module: "{module.name}"')
                
                #add it to the list to iterate later
                self.crModules.append(module)
            except Exception as e:
                print(f"\t{fail} Failed to import analysis module at {moduleFile}")
                print(e)

        self.crModules.sort(key=lambda x:x.priority)


















