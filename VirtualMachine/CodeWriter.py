
def writeArithmetic(command,count=0):
    biArithCommand = {"add": "M = M+D",
                      "sub": "M = M-D",
                      "neg": "M = -M" ,
                      "and": "M = M&D",
                      "or" : "M = M|D",
                      "not": "M = !M" }
    
    biCompareCommand = {"gt": "D;JGT",
                        "lt": "D;JLT",
                        "eq": "D;JEQ"}
    
    label = command["arg1"].upper()+"_"+str(count)
    
    s  = ""
    if command["arg1"] in ["add", "sub", "and", "or"]:
        s += "@SP"
        s += "AM = M-1" # decrease SP
        s += "D = M"
        s += "@SP"
        s += "AM = M-1" # decrease SP
        s += biArithCommand[command["arg1"]]
        
    elif command["arg1"] in ["neg","not"]:
        s += "@SP"
        s += "AM = M-1" # decrease SP
        s += biArithCommand[command["arg1"]]
    
    else:
        s += "@SP"
        s += "AM = M-1" # decrease SP
        s += "D = M"
        s += "@SP"
        s += "AM = M-1"
        s += "D = M-D"
        s += "@IS_"+label
        s += "D;"+biCompareCommand[command["arg1"]]
        s += "@SP"
        s += "A = M"
        s += "M = 0"
        s += "@INC_SP_"+label
        s += "0;JMP"
        s += "(IS_"+label+")"
        s += "@SP"
        s += "A = M"
        s += "M = -1"
        s += "(INC_SP_"+label+")"
    
    s += "@SP"
    s += "M = M+1" # increase SP
    return s

def writePush(command,filename):
    segmentBase = {"local"   : "LCL",
                   "argument": "ARG",
                   "this"    : "THIS",
                   "that"    : "THAT",
                   "temp"   : "R5"}

    segment = command["arg1"]
    index = command["arg2"]

    s = ""
    if segment == "constant":
        s += "@"+index
        s += "D = A"

    elif segment in segmantBase:
        s += "@"+segmantBase[segment]
        
        if segment == "temp":
            s += "D = A"
        else:
            s += "D = M"
        
        s += "@"+index
        s += "D = D+A"
        s += "A = D"
        s += "D = M"

    elif segment == "pointer" and index == "0":
        s += "@THIS"
        s += "D = M"
    
    elif segment == "pointer" and index == "1":
        s += "@THAT"
        s += "D = M"

    elif segment == "static":
        s += "@"+filename+"."+index
        s += "D = M"
        
    s += "@SP"
    s += "A = M"
    s += "M = D"
    s += "@SP"
    s += "M = M+1"
    return s

def writePop(command,filename):
    segmentBase = {"local"   : "LCL",
                   "argument": "ARG",
                   "this"    : "THIS",
                   "that"    : "THAT",
                   "temp"   : "R5"}

    segment = command["arg1"]
    index = command["arg2"]

    s = ""
    s += "@SP"
    s += "M = M-1"
    
    if segment == "static":
        s += "@SP"
        s += "A = M"
        s += "D = M"
        s += "@"+filename+"."+index
        s += "M = D"
        return s

    if segment in segmentBase:
        s += "@"+segmentBase[segment]

        if segmentBase == "temp":
            s += "D = A"
        else:
            s += "D = M"
        
        s += "@"+index
        s += "D = D+A"

    elif segment == "pointer" and index=="0":
        s += "@THIS"
        s += "D = A"

    elif segment == "pointer" and index=="1":
        s += "@THAT"
        s += "D = A"

    s += "@R13"
    s += "M = D"
    s += "@SP"
    s += "A = M"
    s += "D = M"
    s += "@R13"
    s += "A = M"
    s += "M = D"
    return s