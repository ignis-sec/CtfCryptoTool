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
info_start = "\033[94m"
reset = "\033[0m"


#check if a module is pending dependecies
def checkPrequisites(module,results,shared,verbosity):
    bIsUnmet=False
    if(hasattr(module,"prequisites")):
        for dep in module.prequisites:
            if dep not in results and dep not in shared:
                if(verbosity>=2):
                    print(f"{warn} Unmet dependency {dep} for {module.name}")
                    if(verbosity>=3):
                        print(shared)
                        print(results)
                bIsUnmet=True
    return bIsUnmet




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
        self.removedModules=[]
                
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
        if(self.key): results["key"]=self.key
        if(self.plain): results["plain"]=self.plain
        
        #cutoff
        if(depth==self.depth):
            print(f"{fail} Depth limit reached.")
            return

        #modules with unmet prequisites
        modulePending = []

        modulePending.extend(self.anModules)
        if(self.verbosity): print(f"{warn} Starting the analysis step.")
        
        
        while(len(modulePending)):
            numPending = len(modulePending)
            if(self.verbosity>=3):
                print(f"{numPending} modules pending.")
            ### iterate and call each modules analysis function
            for module in modulePending:

                #check if all module dependecies are met
                bIsUnmet=checkPrequisites(module,results,self.sharedData,self.verbosity)
                
                #if there are unmet prequisites, don't run the module
                if(bIsUnmet): continue
                else: modulePending.remove(module)
                
                #check analysis success
                res = module.analyse(results,cipher,ignore=self.ignore, shared=self.sharedData)
                if(res):
                    if(self.verbosity>=2): print(module.success)
                else:
                    if(self.verbosity): print(module.fail)   

                #if module has shared objects, import them to the shared bin
                if(hasattr(module,"share")):
                    for obj in module.share:
                        if(obj not in self.sharedData): self.sharedData[obj] = getattr(module,obj)

            #if number of pending modules is the same, there is a missing dependency, or a deadlock. Stop the analysis here.
            if(numPending==len(modulePending)):
                #dependency loop, cant unstuck
                print(f"{fail} Following modules had unmet prequisites and is removed from the module list:")
                for module in modulePending:
                    print(f"\t{module.name}")
                    self.anModules.remove(module)
                    self.removedModules.append(module)
                break

        
        if(self.verbosity): 
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

            bIsUnmet=checkPrequisites(module,results,self.sharedData,self.verbosity)
            if(bIsUnmet): continue
            
            #forward check for each encryption depending on our analysis. Don't bother if it doesn't pass the forward checks. 
            if(not module.check(results,key=self.key,plain=self.plain,text=cipher, shared=self.sharedData, trace=trace)):
                if(self.verbosity>=2): print(f"{warn} Failed primary check for {module.name}")
                continue
        
            #if forward check passes, attempt to decode with the module
            try:
                res = module.decrypt(cipher,key=self.key,plain=self.plain, shared=self.sharedData, result=results)
                # module should return false if it successfully decrypts, but result looks like nonsense.
                if(not res):
                    if(self.verbosity>=2): print(f"{warn} Failed secondary check for {module.name}")
                else:
                    if(self.plainMode):
                        #passed all the checks, but still not the plaintext we were expecting
                        if(re.match(self.plain,res)):
                            #Matching expected flag format, finalise
                            if(self.verbosity>=3):
                                print(f"{success_start}#######################################################{reset}")
                                print(f"{success_start}#####################POSSIBLE RESULT###################{reset}")
                                print(f"{success_start}#######################################################{reset}")
                            print(f"{success_start}Current stack: {trace}-->{module.name}-->plain{reset}")
                            print(f"{success_start}Stack result:{reset} {res}")
                            print(f"{success} Expected plaintext found. Stopping")
                            print(f"{info} total iterations:{self.counter}")
                            if(len(self.removedModules)):
                                print(f"{warn} Some of your dependecies are missing, and following modules were ignored:")
                                for module in self.removedModules:
                                    print(f"\t{module.name}")
                            self.resultFound=True
                            return
                        else:
                            #looks like a successfull decryption, but not matching the flag format. Output, but continue.
                            #It might be an intermediate step, or flag without proper formatting.
                            if(self.verbosity>=3):
                                print(f"{warn_start}#######################################################{reset}")
                                print(f"{warn_start}#####################POSSIBLE RESULT###################{reset}")
                                print(f"{warn_start}#######################################################{reset}")
                            print(f"{info_start}Current stack: {trace}-->{module.name}{reset}")
                            print(f"{info_start}Stack result:{reset} {res}")
                            if(self.verbosity): print(f"{warn} Missing expected plaintext. Continuing.")
                            self.analyseCipher(res,depth+1,trace+"-->" + module.name)
                    else:
                        #no plain given
                        print(f"{success} {module.name} returned: {res}")
            #most likely module.decrypt failed
            except Exception as e:
                print(e)
                if(self.verbosity): print(f"{fail} Failed to use {module.name}")
        if(not self.resultFound and self.plainMode): 
            print(f"{info} Stack is out of ideas ¯\\_(ツ)_/¯")







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

        self.crModules.sort(key=lambda x:x.priority, reverse=True)







    def loadHelperModules(self):
        helperPath = os.path.join(self.crModuleFolder,"helpers/")
        self.hpModuleFiles = os.listdir(helperPath)
        for moduleFile in self.hpModuleFiles:
            #ignore non .py files
            if not moduleFile.endswith(".py"):
                continue

            #strip file extension
            moduleName = moduleFile.replace('.py', '')
            try:
                #import module from the module folder
                module = importlib.machinery.SourceFileLoader(moduleName, os.path.join(helperPath, moduleFile)).load_module()
                if(self.verbosity): print(f'\t{success} Imported module: "{module.name}"')
                
                #add it to the list to iterate later
                self.crModules.append(module)
            except Exception as e:
                print(f"\t{fail} Failed to import analysis module at {moduleFile}")
                print(e)

        self.crModules.sort(key=lambda x:x.priority, reverse=True)


















