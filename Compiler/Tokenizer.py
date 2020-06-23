import re
import sys

def tokenize(text):
    #print("Original")
    #print(text)
    text = re.sub(r"//.*\n"," ",text)
    text = re.sub(r"/\*.*\*/", " ",text)
    #print("Remove Comments")
    #print(text)
    text = text.replace("{"," { ")
    text = text.replace("}"," } ")
    text = text.replace("["," [ ")
    text = text.replace("]"," ] ")
    text = text.replace("("," ( ")
    text = text.replace(")"," ) ")
    text = text.replace("."," . ")
    text = text.replace(","," , ")
    text = text.replace(";"," ; ")
    text = text.replace("+"," + ")
    text = text.replace("-"," - ")
    text = text.replace("*"," * ")
    text = text.replace("/"," / ")
    text = text.replace("&"," & ")
    text = text.replace("|"," | ")
    text = text.replace("~"," ~ ")
    text = text.replace("<"," < ")
    text = text.replace(">"," > ")
    text = text.replace("="," = ")
    #print("Spacing")
    #print(text)

    # replace String with space to no sapce ver
    def replace_(text):
        return text.replace(" ","#")
    strings = re.findall(r'".*"',text)
    for s in strings:
        text = re.sub(s,replace_(s),text)
    
    words = re.split(r"\s+",text)
    words = [word for word in words if word]
    
    # restore String with space
    def replaceS(text):
        return text.replace("#"," ")
    pat = re.compile(r'".*"')
    for i in range(len(words)):
        if pat.match(words[i]):
            words[i] = replaceS(words[i])

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

def writeTokensXML(tokens,path):
    symbolConvert = {
        "<":"&lt;",
        ">":"&gt;",
        "&":"&amp;"
    }
    with open(path+".xml","w") as f:
        f.write("<tokens>\n")
        for token in tokens:
            if token["Type"] == "KEYWORDS":
                words = token["token"]
                f.write("<keyword> "+words+" </keyword>\n")
            elif token["Type"] == "SYMBOLS":
                if token["token"] in symbolConvert:
                    word = symbolConvert[token["token"]]
                else:
                    word = token["token"]
                f.write("<symbol> "+word+" </symbol>\n")
            elif token["Type"] == "INT_CONST":
                word = token["token"]
                f.write("<integerConstant> "+word+" </integerConstant>\n")
            elif token["Type"] == "STRING_CONST":
                word = token["token"][1:-1]
                f.write("<stringConstant> "+word+" </stringConstant>\n")
            else:
                word = token["token"]
                f.write("<identifier> "+word+" </identifier>\n")
        f.write("</tokens>")

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as f:
        text = f.read()
    tokens = tokenize(text)
    writeTokensXML(tokens,path[:-5])