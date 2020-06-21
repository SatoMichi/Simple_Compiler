
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
            self.writeToken()
        while self.tokens[self.count]["token"] in ["static","field"]:
            self.compileClassVarDec()
        while self.tokens[self.count]["token"] in ["constructor","method","function"]:
            self.compileSubroutine()
        self.writeToken()
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
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass


            

