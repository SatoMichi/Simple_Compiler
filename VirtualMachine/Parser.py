import re

def parser(code,filename):
    code = re.sub(r"//.*","",code)
    code = code.split(r"\s+")
    result = {"Type":"", "arg1":"", "arg2":"", "filename": filename}
    result["Type"] = commandType(code)
    result["arg1"] = commandArg1(code,result["Type"])
    result["arg2"] = commandArg2(code,result["Type"])
    return result

def commandType(code):
    arithCode = ["add","sub","neg","eq","gt","lt","and","or","not"]
    if code[0] in arithCode:
        return "C_ARITHMETIC"
    elif code[0] == "push":
        return "C_PUSH"
    elif code[0] == "pop":
        return "C_POP"
    elif code[0] == "label":
        return "C_LABEL"
    elif code[0] == "goto":
        return "C_GOTO"
    elif code[0] == "if-goto":
        return "C_IF"
    elif code[0] == "function":
        return "C_FUNCTION"
    elif code[0] == "return":
        return "C_RETURN"
    elif code[0] == "call":
        return "C_CALL"
    else:
        return "UNKNOWN"

def commandArg1(code,ctype):
    if ctype == "C_RETURN" or ctype == "UNKNOWN":
        return ""
    elif ctype == "C_ARITHMETIC"::
        return code[0]
    else:
        return code[1]

def commandArg2(code,ctype):
    if ctype == "C_PUSH" or ctype == "C_POP" or ctype == "C_FUNCTION" or ctype == "C_CALL":
        return code[2]
    else:
        return ""
