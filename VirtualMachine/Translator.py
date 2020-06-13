from Parser import parser
from CodeWriter import writeArithmetic, writePush, writePop
import os
import sys

class VM_Translator:
    def __init__(self,path):
        self.files = []
        if ".vm" in path:
            self.files.append(path)
        else:
            os.chdir(path) 
            for filepath in os.listdir():
                self.files.append(filepath)
        self.asmcode = ""
    
    def parseFiles(self):
        self.parsed = []
        for filename in self.files:
            with open(filename) as vmcode:
                for line in vmcode.readlines():
                    self.parsed.append(parser(line,filename))
        self.parsed = [parsed for parsed in self.parsed if not parsed["Type"] == "UNKNOWN"]

    def translate(self):
        for line in self.parsed:
            if line["Type"] == "C_ARITHMETIC":
                self.asmcode += writeArithmetic(line)
            elif line["Type"] == "C_PUSH":
                self.asmcode += writePush(line)
            elif line["Type"] == "C_POP":
                self.asmcode += writePop(line)
    
    def write(self,path):
        with open(path,"w") as f:
            f.write(self.asmcode)

if __name__ == "__main__":
    pathi = sys.argv[1]
    patho = sys.argv[2]
    vm = VM_Translator(pathi)
    vm.parseFiles()
    vm.translate()
    vm.write(patho)