
class CodeWriter:
    def __init__(self):
        self.count = {"gt":0, "lt":0, "eq":0}

    def writeArithmetic(self,command):
        biArithCommand = {"add": "M = M+D",
                        "sub": "M = M-D",
                        "neg": "M = -M" ,
                        "and": "M = M&D",
                        "or" : "M = M|D",
                        "not": "M = !M" }
        
        biCompareCommand = {"gt": "D;JGT",
                            "lt": "D;JLT",
                            "eq": "D;JEQ"}
        
        s  = ""
        if command["arg1"] in ["add", "sub", "and", "or"]:
            s += "@SP" + "\n"
            s += "AM = M-1" + "\n" # decrease SP
            s += "D = M" + "\n"
            s += "@SP" + "\n"
            s += "AM = M-1" + "\n" # decrease SP
            s += biArithCommand[command["arg1"]] + "\n"
            
        elif command["arg1"] in ["neg","not"]:
            s += "@SP" + "\n"
            s += "AM = M-1" + "\n" # decrease SP
            s += biArithCommand[command["arg1"]] + "\n"
        
        else:
            label = command["arg1"].upper()+"_"+str(self.count[command["arg1"]])
            
            s += "@SP" + "\n"
            s += "AM = M-1" + "\n" # decrease SP
            s += "D = M" + "\n"
            s += "@SP" + "\n"
            s += "AM = M-1" + "\n"
            s += "D = M-D" + "\n"
            s += "@IS_"+label + "\n"
            s += biCompareCommand[command["arg1"]] + "\n"
            s += "@SP" + "\n"
            s += "A = M" + "\n"
            s += "M = 0" + "\n"
            s += "@INC_SP_"+label + "\n"
            s += "0;JMP" + "\n"
            s += "(IS_"+label+")" + "\n"
            s += "@SP" + "\n"
            s += "A = M" + "\n"
            s += "M = -1" + "\n"
            s += "(INC_SP_"+label+")" + "\n"
            self.count[command["arg1"]] += 1
        
        s += "@SP" + "\n"
        s += "M = M+1" + "\n" # increase SP
        return s

    def writePush(self,command):
        segmentBase = {"local"   : "LCL",
                       "argument": "ARG",
                       "this"    : "THIS",
                       "that"    : "THAT",
                       "temp"   : "R5"}

        segment = command["arg1"]
        index = command["arg2"]
        filename = command["filename"]

        s = ""
        if segment == "constant":
            s += "@"+index + "\n"
            s += "D = A" + "\n"

        elif segment in segmentBase:
            s += "@"+segmentBase[segment] + "\n"
            
            if segment == "temp":
                s += "D = A" + "\n"
            else:
                s += "D = M" + "\n"
            
            s += "@"+index + "\n"
            s += "D = D+A" + "\n"
            s += "A = D" + "\n"
            s += "D = M" + "\n"

        elif segment == "pointer" and index == "0":
            s += "@THIS" + "\n"
            s += "D = M" + "\n"
        
        elif segment == "pointer" and index == "1":
            s += "@THAT" + "\n"
            s += "D = M" + "\n"

        elif segment == "static":
            s += "@"+filename+"."+index + "\n"
            s += "D = M" + "\n"
            
        s += "@SP" + "\n"
        s += "A = M" + "\n"
        s += "M = D" + "\n"
        s += "@SP" + "\n"
        s += "M = M+1" + "\n"
        return s

    def writePop(self,command):
        segmentBase = {"local"   : "LCL",
                       "argument": "ARG",
                       "this"    : "THIS",
                       "that"    : "THAT",
                       "temp"   : "R5"}

        segment = command["arg1"]
        index = command["arg2"]
        filename = command["filename"]

        s = ""
        s += "@SP" + "\n"
        s += "M = M-1" + "\n"
        
        if segment == "static":
            s += "@SP" + "\n"
            s += "A = M" + "\n"
            s += "D = M" + "\n"
            s += "@"+filename+"."+index + "\n"
            s += "M = D" + "\n"
            return s

        if segment in segmentBase:
            s += "@"+segmentBase[segment] + "\n"

            if segmentBase == "temp":
                s += "D = A" + "\n"
            else:
                s += "D = M" + "\n"
            
            s += "@"+index + "\n"
            s += "D = D+A" + "\n"

        elif segment == "pointer" and index=="0":
            s += "@THIS" + "\n"
            s += "D = A" + "\n"

        elif segment == "pointer" and index=="1":
            s += "@THAT" + "\n"
            s += "D = A" + "\n"

        s += "@R13" + "\n"
        s += "M = D" + "\n"
        s += "@SP" + "\n"
        s += "A = M" + "\n"
        s += "D = M" + "\n"
        s += "@R13" + "\n"
        s += "A = M" + "\n"
        s += "M = D" + "\n"
        return s