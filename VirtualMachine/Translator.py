from Parser import parser
from CodeWriter import writeArithmetic, writePush, writePop
import os

class VM_Translator:
    def __init__(self,path):
        self.files = []
        if ".vm" in path:
            self.files.append(path)
        else:
            os.chdir(path)
            for f in os.listdir():
                self.files.append(f)
        self.asmcode = ""
    
    def parseFiles(self):
        self.parsed = []
        for f in self.files:
            with open(f) as code:
                for line in code.readlines():
                    self.parsed.append(parse(line))
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