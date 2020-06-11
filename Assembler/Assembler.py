from Parser import parser
from Code import rowCoder
from SymbolTable import SymbolTable
import sys

class Assembler:
    def __init__(self):
        self.rowcodes = []
        self.table = SymbolTable()
        const   = [ "SP","LCL","ARG","THIS","THAT",
                    "R0", "R1", "R2", "R3", "R4", "R5", "R6","R7",
                    "R8","R9","R10","R11","R12","R13","R14","R15",
                    "SCREEN","KBD"]
        address = [ 0,1,2,3,4,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16384,24576]
        
        for s,n in zip(const,address):
            self.table.addEntry(s,n)

    def parse(self,codes):
        self.parsed = [parser(c) for c in codes]
    
    def readLabel(self,codes):
        pc = 0
        for line in self.parsed:
            if line["Type"] == "L_COMMAND":
                self.table.addEntry(line["symbol"],pc)
            elif line["Type"] == "A_COMMAND" or line["Type"] == "C_COMMAND":
                pc += 1
            else:
                pass
    
    def readVar(self,codes):
        address = 16
        for line in self.parsed:
            if line["Type"] == "COMMENT" or line["Type"] == "L_COMMAND":
                continue
            elif line["Type"] == "A_COMMAND" and not line["symbol"].isdigit():
                if not self.table.contains(line["symbol"]):
                    self.table.addEntry(line["symbol"],address)
                    address += 1
                line["symbol"] = str(self.table.getAddress(line["symbol"]))
                
            self.rowcodes.append(line)
    
    def assemble(self,codes):
        self.parse(codes)
        self.readLabel(codes)
        self.readVar(codes)
        self.binary = [rowCoder(line) for line in self.rowcodes]
        return self.binary

    def read(self,path):
        with open(path) as f:
            codes = [line for line in f.readlines()]
        return codes

    def write(self,path):
        with open(path,"w") as f:
            for code in self.binary:
                f.write(code+"\n")

if __name__ == "__main__":
    pathin = sys.argv[1]
    pathout = sys.argv[2]
    assembler = Assembler()
    codes = assembler.read(pathin)
    rowCodes = assembler.assemble(codes)
    assembler.write(pathout)

                        
                




