import re

def parser(code):
    # remove all the spaces
    code = re.sub(r"\s+","",code)
    # prepare parsed info
    result = {"Type":"","symbol":"","dst":"","comp":"","jmp":""}
    result["Type"] = commandType(code)
    result["symbol"] = extractSymbol(code,result["Type"])
    # if command type is C, extract "dst=comp;jmp"
    if result["Type"] == "C_COMMAND":
        result["dst"] = extractDst(code)
        result["comp"] = extractComp(code)
        result["jmp"] = extractJmp(code)

    return result

def commandType(code):
    if code[0] == "@":
        return "A_COMMAND"
    elif code[0] == "(":
        return "L_COMMAND"
    else:
        return "C_COMMAND"

def extractSymbol(code,ctype):
    if ctype == "A_COMMAND":
        return str(code[1:])
    elif ctype == "L_COMMAND":
        return str(code[1:-1])
    else:
        return ""

def extractDst(code):
    if "=" in code:
        return str(code.split("=")[0])
    else:
        return ""

def extractComp(code):
    if "=" in code and ";" in code:
        return str(re.split(r"=|;",code)[1])
    elif "=" in code:
        return str(code.split("=")[1])
    elif ";" in code:
        return str(code.split(";")[0])
    else:
        return code

def extractJmp(code):
    if ";" in code:
        return str(code.split(";")[-1])
    else:
        return ""
