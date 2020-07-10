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
        self.label_count = {"if":0, "while":0}
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
        self.label_count["if"] = 0
        self.label_count["while"] = 0

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
            num_locals += 1
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
            # store result to temp 0
            self.vmcode += VMWriter.writePop('temp','0')
            # store address of array to THAT
            self.vmcode += VMWriter.writePop('pointer','1')
            # restore result
            self.vmcode += VMWriter.writePush('temp','0')
            # save result to THAT
            self.vmcode += VMWriter.writePop('that','0')
        self.advance()                  # ;

    def compileWhile(self):
        # label whileStart
        self.vmcode += VMWriter.writeLabel("WHILE_START_"+self.label_count["while"])
        self.advance()           # while
        self.advance()           # (
        self.compileExpression()
        self.advance()           # )
        # if not exp == True: goto whileEnd
        self.vmcode += VMWriter.writeArithmetic("~")
        self.vmcode += VMWriter.writeIfGoto("WHILE_END_"+self.label_count["while"])
        self.advance()           # {
        self.compileStatements()
        # goto whileStart
        self.vmcode += VMWriter.writeGoto("WHILE_START_"+self.label_count["while"])
        self.advance()           # }
        # label whileEnd
        self.vmcode += VMWriter.writeLabel("WHILE_END_"+self.label_count["while"])
        self.label_count["while"] += 1

    def compileReturn(self):
        self.advance()       # return
        if not self.tokens[self.count]["token"] == ";":
            # push result to stack
            self.compileExpression()
        else:
            # push constant 0 to stack for void
            self.vmcode += VMWriter.writePush("constant","0")
        self.advance()       # ;
        self.vmcode += VMWriter.writeReturn()

    def compileIf(self):
        self.advance()           # if
        self.advance()           # (
        self.compileExpression()
        self.advance()           # )
        # if expression: goto IF_TRUE
        self.vmcode += VMWriter.writeIfGoto("IF_TRUE_"+self.label_count["if"])
        # if not expression: goto IF_FALSE
        self.vmcode += VMWriter.writeGoto("IF_FALSE_"+self.label_count["if"])
        # label IF_TRUE
        self.vmcode += VMWriter.writeLabel("IF_TRUE_"+self.label_count["if"])
        self.advance()           # {
        self.compileCondStatements()
        self.advance()           # }
        # else exist
        if self.tokens[self.count]["token"] == "else":
            self.advance()       # else
            self.advance()       # {
            # if excuted if part, got IF_END
            self.vmcode += VMWriter.writeGoto("IF_END_"+self.label_count["if"])
            # label IF_FALSE
            self.vmcode += VMWriter.writeLabel("IF_FALSE_"+self.label_count["if"])
            self.compileCondStatements()
            # label IF_END
            self.vmcode += VMWriter.writeLabel("IF_END_"+self.label_count["if"])
            self.advance()          # }
        else:
            # label IF_FALSE
            self.vmcode += VMWriter.writeLabel("IF_FALSE_"+self.label_count["if"])

    def compileCondStatements(self):
        # nested if
        if self.tokens[self.count]["token"] == "if":
            self.label_count["if"] += 1
            self.compileStatements()
            self.label_count["if"] -= 1
        else:
            self.compileStatements()

    def compileExpression(self):
        # Order of operations is from front to back
        self.compileTerm()
        while self.tokens[self.count]["token"] in ["+","-","*","/","&","|","<",">","="]:
            op = self.takeWord()       # op
            self.compileTerm()
            # execute op
            if op == "*":
                self.vmcode += VMWriter.writeCall("Math.multiply",2)
            elif op == "/":
                self.vmcode += VMWriter.writeCall("Math.divide",2)
            else:
                self.vmcode += VMWriter.writeArithmetic(op)

    def compileTerm(self):
        # intConst
        if self.tokens[self.count]["Type"]=="INT_CONST":
            i = self.takeWord()
            self.vmcode += VMWriter.writePush("constant",i)
        # StringConst
        elif self.tokens[self.count]["Type"]=="STRING_CONST":
            s = self.takeWord()
            self.compileString(s)
        # KeyConst
        elif self.tokens[self.count]["Type"]=="KEYWORDS":
            word = self.takeWord()
            if word == "null":
                self.vmcode += VMWriter.writePush("constant",0)
            elif word =="true":
                self.vmcode += VMWriter.writePush("constant",0)
                self.vmcode += VMWriter.writeArithmetic("~")
            elif word=="false":
                self.vmcode += VMWriter.writePush("constant",0)
            elif word=="this":
                self.vmcode += VMWriter.writePush("this",0)
        # varName
        elif self.tokens[self.count]["Type"]=="IDENTIFIER":
            var = self.takeWord()
            symbol = self.findSymbol(var)
            segment = symbol['kind']
            index = symbol['index']
            self.vmcode += VMWriter.writePush(segment,index)
        # (exp)
        elif self.tokens[self.count]["token"] == "(":
            self.advance()           # (
            self.compileExpression()
            self.advance()           # )
        # unaryOP term
        elif self.tokens[self.count]["token"] in ["-","~"]:
            op = self.takeWord()        # op
            self.compileTerm()
            self.vmcode += VMWriter.writeArithmetic(op)
        # Array element
        elif self.tokens[self.count+1]["token"] == "[":
           self.compileArrayEXP()
        # Subroutine Call
        elif self.tokens[self.count+1]["token"] in ["(","."]:
            self.compileSubroutineCall()
        
    def compileString(self,s):
        # use standard library String
        str_len = len(s)
        self.vmcode += VMWriter.writePush("constant",str_len)
        self.vmcode += VMWriter.writeCall("String.new",1)
        for c in self.tokens[self.count]["token"]:
            if not c == "\"":
                asciic = ord(c)
                self.vmcode += VMWriter.writePush("constant",asciic)
                self.vmcode += VMWriter.writeCall("String.appendChar",2)

    def compileSubroutineCall(self):
        subroutine_name = ""
        if self.tokens[self.count+1]["token"] == ".":
            for i in range(3):
                subroutine_name += self.takeWord()      # (className|varName) . subroutineName
        else:
            subroutine_name = self.takeWord()           # subroutineName 
        self.advance()                                  # (
        num_args = self.compileExpressionList()
        self.vmcode += VMWriter.writeCall(subroutine_name, num_args)
        self.advance()                                  # ) 

    def compileArrayEXP(self):
        symbolName = self.takeWord()            # varName
        symbol = self.findSymbol(symbolName)
        self.advance()                          # [
        self.compileExpression()
        # push base address to stack
        self.vmcode += VMwriter.writePush("local",symbol['index'])
        # add index(expression result) and base addresses
        self.vmcode += VMwriter.writeArithmetic('+')
        # pop address into THAT
        self.vmcode += VMwriter.writePop("pointer","1")
        # push value to stack
        self.vmcode += VMwriter.writePush("that","0")
        self.advance()                          # ]

    def compileExpressionList(self):
        num_args = 0
        if self.tokens[self.count]["token"] == ")":
            return num_args
        else:
            self.compileExpression()
            num_args += 1
            while self.tokens[self.count]["token"] == ",":
                self.advance()               # ,
                self.compileExpression()
                num_args += 1
            return num_args

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
