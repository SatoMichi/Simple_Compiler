
class ParserXML:
    def __init__(self,tokens):
        self.tokens = tokens
        self.count = 0
        self.xml = ""
    
    def writeToken(self):
        symbolConvert = {"<":"&lt;",">":"&gt;","&":"&amp;"}
        token = self.tokens[self.count]
        if token["Type"] == "KEYWORDS":
                words = token["token"]
                self.xml += "<keyword> "+words+" </keyword>\n"
            elif token["Type"] == "SYMBOLS":
                if token["token"] in symbolConvert:
                    word = symbolConvert[token["token"]]
                else:
                    word = token["token"]
                self.xml += "<symbol> "+word+" </symbol>\n"
            elif token["Type"] == "INT_CONST":
                word = token["token"]
                self.xml += "<integerConstant> "+word+" </integerConstant>\n"
            elif token["Type"] == "STRING_CONST":
                word = token["token"][1:-1]
                self.xml += "<stringConstant> "+word+" </stringConstant>\n"
            else:
                word = token["token"]
                self.xml += "<identifier> "+word+" </identifier>\n"
        self.count += 1

    def complieClass(self):
        self.xml += "<class>\n"
        for i in range(3):
            self.writeToken()  # class className {
        while self.tokens[self.count]["token"] in ["static","field"]:
            self.compileClassVarDec()
        while self.tokens[self.count]["token"] in ["constructor","method","function"]:
            self.compileSubroutine()
        self.writeToken()       # }
        self.xml += "</class>\n"

    def compileClassVarDec(self):
        self.xml += "<classVarDec>\n"
        for i in range(2):
            self.writeToken() # (static|field) type 
        self.writeToken()     # VarName
        while not self.tokens[self.count]["token"] == ";"
            self.writeToken() # ,
            self.writeToken() # varName
        self.writeToken()     # ;
        self.xml += "</classVarDec>\n"
    
    def compileSubroutine(self):
        self.xml += "<subroutineDec>\n"
        for i in range(4):
            self.writeToken()       # (constructor|method|function) type subroutineName (
        self.complieParameterList()
        self.writeToken()           # )
        self.xml += "<subroutineBody>\n"
        self.writeToken()           # {
        while self.tokens[self.count]["token"] in ["var"]:
            self.compileVarDec()
        self.compileStatements()
        self.writeToken()           # }
        self.xml += "</subroutineBody>\n"
        self.xml += "</subroutineDec>\n"
    
    def complieParameterList(self):
        self.xml += "<ParameterList>\n"
        if self.tokens[self.count]["token"] == ")": # has no parameters
            pass
        else: 
            for i in range(2):
                self.writeToken()                   # type VarName
            while self.tokens[self.count]["token"] == ",":
                for i in range(3):
                    self.writeToken()               # , type VarName
        self.xml += "</ParameterList>\n"

    def compileVarDec(self):
        self.xml += "<VarDec>\n"
        for i in range(3):
            self.writeToken()       # var type VarName
        while self.tokens[self.count]["token"] == ",":
            for i in range(2):
                self.writeToken()   # , VarName
        self.writeToken()           # ;
        self.xml += "</VarDec>\n"

    def compileStatements(self):
        self.xml += "<Statements>\n"
        if self.tokens[self.count] == "}":  # no statements
            pass
        else:
            while self.tokens[self.count] in ["do","let","while","return","if"]:
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
        self.xml += "<Statements>\n"

    def compileDo(self):
        self.xml += "<doStatement>\n"
        self.writeToken()               # do
        self.compileSubroutineCall()
        self.writeToken()               # ;
        self.xml += "</doStatement>\n"

    def compileLet(self):
        self.xml += "<letStatement>\n"
        for i in range(2):
            self.writeToken()           # let varName
        if self.tokens[self.count]["token"] == "[":
            self.writeToken()           # [
            self.compileExpression()
            self.writeToken()           # ]
        self.writeToken()               # =
        self.compileExpression()
        self.writeToken()               # ;
        self.xml += "</letStatement>\n"

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
        elif self.tokens[self.count+1]["token"] == "(":
            self.compileSubroutineCall()
        else:
            self.writeToken()           # (intConst|StringConst|KeyConst|varName)
        self.xml += "</term>\n"
    
    def compileSubroutineCall(self):
        self.xml += "<subroutineCall>\n"
        if self.tokens[self.count+1]["token"] == ".":
            for i in range(3):
                self.writeToken()               # (className|varName) . subroutineName
        else:
            self.writeToken()                   # subroutineName 
        self.writeToken()                       # (
        self.compileExpressionList()
        self.writeToken()                       # ) 
        self.xml += "</subroutineCall>\n"

    def compileExpressionList(self):
        self.xml += "<expressionList>\n"
        if self.tokens[self.count]["token"] == ")":
            pass
        else:
            self.compileExpression()
            while self.tokens[self.count]["token"] == ",":
                for i in range(2):
                    self.writeToken()           # ,
                    self.compileExpression()
        self.xml += "</expressionList>\n"