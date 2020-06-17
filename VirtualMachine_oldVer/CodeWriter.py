
class CodeWriter:
    def __init__(self):
        self.count = {"gt":0, "lt":0, "eq":0}
        self.funcId = -1
        self.callId = -1

    def boostrap(self):
        # initializing the VM
        s = ""
        s += "@256" + "\n"
        s += "D = A" + "\n"
        s += "@SP" + "\n"
        s += "M = D" + "\n"
        # call the starting function
        s += self.writeFuncCall({"Type": "C_CALL", "arg1": "Sys.init", "arg2": "0"})
        return s

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

            if segment == "temp":
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
    
    def writeLabel(self,command):
        s = ""
        s += "("+command["arg1"]+")" + "\n"
        return s
    
    def writeGoto(self,command):
        s  = ""
        s += "@"+command["arg1"] + "\n"
        s += "0 ; JMP" + "\n"
        return s
    
    def writeIfGoto(self,command):
        s = ""
        s += "@SP" + "\n"
        s += "AM = M-1" + "\n"
        s += "D = M" + "\n"
        s += "@"+command["arg1"] + "\n"
        s += "D ; JNE" + "\n"
        return s
    
    def writeFuncDef(self,command):
        self.funcId += 1
        fid  = str(self.funcId)
        #filename = command["filename"]
        #funcName = filename+"."+command["arg1"]
        funcName = command["arg1"]
        nOfLocal = command["arg2"]

        s = ""
        s += "("+funcName+")" + "\n"
        s += "@"+nOfLocal + "\n"
        s += "D = A" + "\n"
        s += "(LOOP_INIT_LOCAL_"+funcName+"_"+fid+")" + "\n"
        s += "@NO_ARG_"+funcName+"_"+fid + "\n"
        s += "D ; JEQ" + "\n"
        s += "@SP" + "\n"
        s += "A = M" + "\n"
        s += "M = 0" + "\n" # initialize with 0
        s += "@SP" + "\n"
        s += "M = M+1" + "\n"
        s += "D = D-1" + "\n" # decrease counter
        s += "@LOOP_INIT_LOCAL_"+funcName+"_"+fid + "\n"
        s += "D ; JNE" + "\n"
        s += "(NO_ARG_"+funcName+"_"+fid+")" + "\n"
        return s
    
    def writeSaveFrame(self):
        segs = ["LCL","ARG","THIS","THAT"]
        s = ""
        for seg in segs:
            s += "@" + seg + "\n"
            s += "D = M" + "\n"
            s += "@SP" + "\n"
            s += "A = M" + "\n"
            s += "M = D" + "\n"
            s += "@SP" + "\n"
            s += "M = M+1" + "\n"
        return s 

    def writeFuncCall(self,command):
        self.callId += 1
        cid = str(self.callId)
        #filename = command["filename"]
        #funcName = filename+"."+command["arg1"]
        funcName = command["arg1"]
        nOfArg = command["arg2"]

        s = ""
        # save return address
        s += "@RETURN_"+funcName+"_"+cid + "\n"
        s += "D = A" + "\n"
        s += "@SP" + "\n"
        s += "A = M" + "\n"
        s += "M = D" + "\n"
        s += "@SP" + "\n"
        s += "M = M+1" + "\n"
        # save each segment and increase SP
        s += self.writeSaveFrame()
        # set new ARG
        s += "@SP" + "\n"
        s += "D = M" + "\n"
        s += "@"+nOfArg + "\n"
        s += "D = D-A" + "\n"
        s += "@5" + "\n"
        s += "D = D-A" + "\n"
        s += "@ARG" + "\n"
        s += "M = D" + "\n"
        # set new LCL
        s += "@SP" + "\n"
        s += "D = M" + "\n"
        s += "@LCL" + "\n"
        s += "M = D" + "\n"
        s += "@"+funcName + "\n"
        s += "0 ; JMP" + "\n"
        s += "(RETURN_"+funcName+"_"+cid+")" + "\n"
        return s

    def writeRestoreFrame(self):
        segs = ["THAT","THIS","ARG","LCL"]
        addr = ["1", "2", "3", "4"]
        s = ""
        for seg, a in zip(segs, addr):
            s += "@"+a + "\n"
            s += "D = A" + "\n"
            s += "@R13" + "\n"
            s += "A = M-D" + "\n"
            s += "D = M" + "\n"
            s += "@"+seg + "\n"
            s += "M = D" + "\n"
        return s

    def writeReturn(self,command):
        s = ""
        # R13 is address of buttom of current stack
        s += "@LCL" + "\n"
        s += "D = M" + "\n"
        s += "@R13" + "\n"
        s += "M = D" + "\n"
        s += "@5" + "\n"
        s += "D = A" + "\n"
        s += "@R13" + "\n"
        s += "A = M-D" + "\n"
        s += "D = M" + "\n"
        # save return address to R14
        s += "@R14" + "\n"
        s += "M = D" + "\n"
        # save function value to top of the caller's stack (address of current ARG[0])
        s += "@SP" + "\n"
        s += "AM = M-1" + "\n"
        s += "D = M" + "\n"
        s += "@ARG" + "\n"
        s += "A = M" + "\n"
        s += "M = D" + "\n"
        # return SP to Original place (address of current ARG[1])
        s += "@ARG" + "\n"
        s += "D = M+1" + "\n"
        s += "@SP" + "\n"
        s += "M = D" + "\n"
        # restore original environment
        s += self.writeRestoreFrame()
        # jumpt to return address
        s += "@R14" + "\n"
        s += "A = M" + "\n"
        s += "0 ; JMP" + "\n"
        return s
