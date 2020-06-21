import re

def tokenize(text):
    words = re.split(r"\s+|//.*\n|//*.*/*/|//*/*.*/*/")
    tokens = []
    for token in words:
        ctype = commandType(token)
        tokens.append({"Type":ctype,"token":token})
    return tokens

keywords = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return"
]

symbols = list("{}[]().,;+-*/&|<>=~")

def commandType(token):
    if token in keywords:
        return "KEYWORDS"
    elif token in symbols:
        return "SYMBOLS"
    elif token.isdigit():
        return "INT_CONST"
    elif token.startswith("\""):
        return "STRING_CONST"
    else:
        return "IDENTIFIER"

def writeTokensXML(tokens):
    symbolConvert = {
        "<":"&lt"
        ">":"&gt"
        "&":"&amp"
    }
    with open("tokens.txt","w") as f:
        f.write("<tokens>\n")
        for token in tokens:
            if token["Type"] == "KEYWORDS":
                words = token["token"]
                f.write("<keyword>"+words+"</keyword>/n")
            elif token["Type"] == "SYMBOLS":
                if token["token"] in symbolConvert:
                    word = symbolConvert[token["token"]]
                else:
                    word = token["token"]
                f.write("<symbol>"+word+"</symbol>\n")
            elif token["Type"] == "INT_CONST":
                word = token["token"]
                f.write("<integerConstant>"+word+"</integerConstant>\n")
            elif token["Type"] == "STRING_CONST":
                word = token["token"][1:-1]
                f.write("<stringConstant>"+word+"</stringConstant>\n")
            else:
                word = token["token"]
                f.write("<identifier>"+word+"</identifier>\n")
        f.write("</tokens>")