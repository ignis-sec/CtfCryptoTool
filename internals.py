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
    def __init__(self,verbosity, analysisFolder, cryptoFolder,key='',plain=''):
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


    def analyseCipher(self,cipher):
        results = {}
        ### iterate and call each module
        print(f"{warn} Starting the analysis step.")
        for module in self.anModules:
            res = module.analyse(results,cipher)
            if(res):
                if(self.verbosity>=2): print(module.success)
            else:
                if(self.verbosity): print(module.fail)

        print(f"{warn} Analysis results:")
        print(results)
        self.findDecipher(results, cipher)

    def findDecipher(self,results, cipher):
        for module in self.crModules:
            if(not module.check(results)):
                if(self.verbosity>=2): print(f"{warn} Failed primary check for {module.name}")
                continue
        
            try:
                res = module.decode(cipher,self.key)
                if(not res):
                    if(self.verbosity>=2): print(f"{warn} Failed secondary check for {module.name}")
                else:
                    if(self.plainMode):
                        if(re.match(self.plain,res)):
                            print(f"{success_start}#######################################################{reset}")
                            print(f"{success_start}#####################POSSIBLE RESULT###################{reset}")
                            print(f"{success_start}#######################################################{reset}")
                            print(f"{success} {module.name} returned: {res}")
                            print(f"{success} Expected plaintext found. Stopping")
                            return
                        else:
                            print(f"{warn_start}#######################################################{reset}")
                            print(f"{warn_start}#####################POSSIBLE RESULT###################{reset}")
                            print(f"{warn_start}#######################################################{reset}")
                            print(f"{success} {module.name} returned: {res}")
                            print(f"{warn} Missing expected plaintext. Continuing.")
                            self.analyseCipher(res)
            except Exception as e:
                print(e)
                if(self.verbosity): print(f"{fail} Failed to use {module.name}")


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
            except:
                print(f"\t{fail} Failed to import analysis module at {moduleFile}")
        

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
            except:
                print(f"\t{fail} Failed to import analysis module at {moduleFile}")


















