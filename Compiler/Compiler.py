from Tokenizer import tokenize
from SymbolTable import SymbolTable
import VMWriter
import sys

class Compiler:
    def __init__(self,path):
        with open(path) as f:
            text = f.read()
        self.tokens = tokenize(text)
        self.count = 0
        self.ClassScope = SymbolTable()
        self.SubroutineScope = SymbolTable()
        self.label_count = 0
        self.vmcode = ""
    
    def writeVMcode(self,path):
        self.complieClass()
        with open(path,"w") as f:
            f.write(self.vmcode)

    def takeWord(self):
        token = self.tokens[self.count]["token"]
        self.count += 1
        return token

    def advance(self):
        self.count += 1

    def compileClass(self):
        self.advance()                      # class
        self.className = self.takeWord()    # className
        self.advance()                      # {
        while self.tokens[self.count]["token"] in ["static","field"]:
            self.compileClassVarDec()
        while self.tokens[self.count]["token"] in ["constructor","method","function"]:
            self.compileSubroutine()
        self.advance()                      # }

    def compileClassVarDec(self):
        symbolKind = self.takeWord()        # (static|field)
        symbolType = self.takeWord()        # type
        symbolName = self.takeWord()        # VarName
        self.ClassScope.define(symbolName, symbolType, symbolKind)
        while not self.tokens[self.count]["token"] == ";":
            self.advance()                  # ,
            symbolName = self.takeWord()    # VarName
            self.ClassScope.define(symbolName, symbolType, symbolKind)
        self.advance()                      # ;
    
    def compileSubroutine(self):
        self.SubroutineScope.reset()
        self.advance()                      # (constructor|method|function)
        self.advance()                      # type
        subroutineName = self.takeWord()    # SubroutineName
        self.advance()                      # (
        self.complieParameterList()
        self.advance()                      # )
        self.advance()                      # {
        num_locals = 0
        while self.tokens[self.count]["token"] in ["var"]:
            num_locals += self.compileVarDec()
        self.vmcode += VMWriter.writeFunction(self.className+"."+subroutineName,num_locals)
        self.compileStatements()
        self.advance()                      # }
    
    def complieParameterList(self):
        if self.tokens[self.count]["token"] == ")": # has no parameters
            pass
        else: 
            symbolKind = "argument"
            symbolType = self.takeWord()            # type
            symbolName = self.takeWord()            # VarName
            self.SubroutineScope.define(symbolName,symbolType,symbolKind)
            while self.tokens[self.count]["token"] == ",":
                self.advance()                      # ,
                symbolType = self.takeWord()        # type
                symbolName = self.takeWord()        # VarName
                self.SubroutineScope.define(symbolName,symbolType,symbolKind)

    def compileVarDec(self):
        symbolKind = "local"
        self.advance()                      # var
        symbolType = self.takeWord()        # type
        symbolName = self.takeWord()        # VarName
        self.SubroutineScope.define(symbolName,symbolType,symbolKind)
        num_locals = 1
        while self.tokens[self.count]["token"] == ",":
            self.advance()                  # ,
            symbolName = self.takeWord()    # VarName
            self.SubroutineScope.define(symbolName,symbolType,symbolKind)
            num_locals = 1
        self.advance()                      # ;
        return num_locals

    def compileStatements(self):
        if self.tokens[self.count] == "}":  # no statements
            pass
        else:
            while self.tokens[self.count]["token"] in ["do","let","while","return","if"]:
                if self.tokens[self.count]["token"] == "do":
                    self.compileDo()
                elif self.tokens[self.count]["token"] == "let":
                    self.compileLet()
                elif self.tokens[self.count]["token"] == "while":
                    self.compileWhile()
                elif self.tokens[self.count]["token"] == "return":
                    self.compileReturn()
                elif self.tokens[self.count]["token"] == "if":
                    self.compileIf()

    def compileDo(self):
        self.advance()                              # do
        caller = self.takeWord()                    # (className|varName) 
        symbol = self.findSymbol(caller)
        self.advance()                              # .
        func = self.takeWord()                      # subroutineName   
        # if object exist, push it in to stack
        if symbol:
            segment = 'local'
            index = symbol['index']
            self.vmcode += VMWriter.writePush(segment,index)
            symbolType = symbol['type']
        else:
            symbolType = caller
        # decide subroutine name
        subroutineName = symbolType+'.'+func
        self.advance()                              # (
        num_args = self.compileExpressionList()
        if symbol:
            # add "this"
            num_args += 1 
        # call the function
        self.vmcode += VMWriter.writeCall(subroutineName,num_args)
        # since this code will not save returned value in to variable, pop it out.
        self.vmcode += VMWriter.writePop('temp','0')

        self.advance()                              # )
        self.advance()                              # ;

    def compileLet(self):
        self.advance()                  # let
        symbolName = self.takeWord()    # varName
        symbol = self.findSymbol(symbolName)
        isArray = self.tokens[self.count]["token"] == "["
        if isArray:
            self.advance()              # [
            # this will push value to stack
            self.compileExpression()
            # push base address
            self.vmcode += VMWriter.writePush(symbol['kind'],symbol['index'])
            # add two addresses
            self.vmcode += VMwriter.writeArithmetic('+')
            self.advance()              # ]
        self.advence()                  # =
        # this will push result to stack
        self.compileExpression()
        if not isArray:
            self.vmcode += VMWriter.writePop(symbol['kind'],symbol['index'])
        else:
            self.vmcode += VMWriter.writePop('temp','0')
            self.vmcode += VMWriter.writePop('pointer','1')
            self.vmcode += VMWriter.writePush('temp','0')
            self.vmcode += VMWriter.writePop(segment='that', index='0')
        self.advance()                  # ;

    def compileWhile(self):
        self.xml += "<whileStatement>\n"
        self.writeToken()           # while
        self.writeToken()           # (
        self.compileExpression()    
        self.writeToken()           # )
        self.writeToken()           # {
        self.compileStatements()
        self.writeToken()           # }
        self.xml += "</whileStatement>\n"

    def compileReturn(self):
        self.xml += "<returnStatement>\n"
        self.writeToken()       # return
        if not self.tokens[self.count]["token"] == ";":
            self.compileExpression()
        self.writeToken()       # ;
        self.xml += "</returnStatement>\n"

    def compileIf(self):
        self.xml += "<ifStatement>\n"
        self.writeToken()           # if
        self.writeToken()           # (
        self.compileExpression()
        self.writeToken()           # )
        self.writeToken()           # {
        self.compileStatements()
        self.writeToken()           # }
        if self.tokens[self.count]["token"] == "else":
            self.writeToken()       # else
            self.writeToken()       # {
            self.compileStatements()
            self.writeToken()       # }
        self.xml += "</ifStatement>\n"

    def compileExpression(self):
        self.xml += "<expression>\n"
        self.compileTerm()
        while self.tokens[self.count]["token"] in ["+","-","*","/","&","|","<",">","="]:
            self.writeToken()       # op
            self.compileTerm()
        self.xml += "</expression>\n"

    def compileTerm(self):
        self.xml += "<term>\n"
        if self.tokens[self.count]["token"] == "(":
            self.writeToken()           # (
            self.compileExpression()
            self.writeToken()           # )
        elif self.tokens[self.count]["token"] in ["-","~"]:
            self.writeToken()           # op
            self.compileTerm()
        elif self.tokens[self.count+1]["token"] == "[":
            self.writeToken()           # varName
            self.writeToken()           # [
            self.compileExpression()
            self.writeToken()           # ]
        elif self.tokens[self.count+1]["token"] in ["(","."]:
            self.compileSubroutineCall()
        else:
            self.writeToken()           # (intConst|StringConst|KeyConst|varName)
        self.xml += "</term>\n"
    
    def compileSubroutineCall(self):
        if self.tokens[self.count+1]["token"] == ".":
            caller = self.takeWord()                    # (className|varName) 
            symbol = self.findSymbol(caller)
            self.advance()                              # .
            func = self.takeWord()                      # subroutineName
        else:
            func = self.takeWord()                      # subroutineName
        
        if symbol:
            segment = 'local'
            index = symbol['index']
            self.vmcode += VMWriter.writePush(segment,index)
            symbolType = symbol['type']
        else:
            symbolType = caller

        subroutineName = symbolType+'.'+func
        self.writeToken()                               # (
        num_args = self.compileExpressionList()
        if symbol:
            # for this
            num_args += 1 
        
        self.vmcode += VMWriter.writeCall(subroutineName,num_args)

        self.vmcode += VMWriter.writePop('temp','0')
        self.writeToken()                               # )

    def compileExpressionList(self):
        self.xml += "<expressionList>\n"
        if self.tokens[self.count]["token"] == ")":
            pass
        else:
            self.compileExpression()
            while self.tokens[self.count]["token"] == ",":
                self.writeToken()               # ,
                self.compileExpression()
        self.xml += "</expressionList>\n"

    def findSymbol(self,symbol):
        if symbol in [s["name"] for s in self.SubroutineScope]:
            return [s["name"] for s in self.SubroutineScope if s["name"] == symbol][0]
        elif symbol in [s["name"] for s in self.ClassScope]:
            return [s["name"] for s in self.ClassScope if s["name"] == symbol][0]
        else:
            return None

if __name__ == "__main__":
    path = sys.argv[1]
    parser = Compiler(path)
    parser.writeVMcode(path[:-5]+".vm")
