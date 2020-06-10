dest2bin = {
    ""   : [0,0,0],
    "A"  : [1,0,0],
    "D"  : [0,1,0],
    "M"  : [0,0,1],
    "MD" : [0,1,1],
    "AM" : [1,0,1],
    "AD" : [1,1,0],
    "AMD": [1,1,1]
}

jmp2bin = {
    ""   : [0,0,0],
    "JGT": [0,0,1],
    "JEQ": [0,1,0],
    "JGE": [0,1,1],
    "JLT": [1,0,0],
    "JNE": [1,0,1],
    "JLE": [1,1,0],
    "JMP": [1,1,1]
}

comp2bin = {
    "0"   : [0,1,0,1,0,1,0],
    "1"   : [0,1,1,1,1,1,1],
    "-1"  : [0,1,1,1,0,1,0],
    "D"   : [0,0,0,1,1,0,0],
    "A"   : [0,1,1,0,0,0,0], "M"   : [1,1,1,0,0,0,0],
    "!D"  : [0,0,0,1,1,0,1],
    "!A"  : [0,1,1,0,0,0,1], "!M"  : [1,1,1,0,0,0,1],
    "-D"  : [0,0,0,1,1,1,1],
    "-A"  : [0,1,1,0,0,1,1],
    "D+1" : [0,0,1,1,1,1,1],
    "A+1" : [0,1,1,0,1,1,1], "M+1" : [1,1,1,0,1,1,1],
    "D-1" : [0,0,0,1,1,1,0],
    "A-1" : [0,1,1,0,0,1,0], "M-1" : [1,1,1,0,0,1,0],
    "D+A" : [0,0,0,0,0,1,0], "D+M" : [1,0,0,0,0,1,0],
    "D-A" : [0,0,1,0,0,1,1], "D-M" : [1,0,1,0,0,1,1],
    "A-D" : [0,0,0,0,1,1,1], "M-D" : [1,0,0,0,1,1,1],
    "D&A" : [0,0,0,0,0,0,0], "D&M" : [1,0,0,0,0,0,0],
    "D|A" : [0,0,1,0,1,0,1], "D|M" : [1,0,1,0,1,0,1]
}

def rowCoder(parse):
    if parse["Type"] == "A_COMMAND":
        return row_a_cmd2bin(parse)
    elif parse["Type"] == "C_COMMAND":
        return row_c_cmd2bin(parse)
    else:
        return ""

def row_a_cmd2bin(parse):
    head = "0"
    num = dec2bin(int(parse["symbol"]))
    return head + num

def row_c_cmd2bin(parse):
    head = "111"
    dstbin = "".join(map(str,dest(parse["dst"])))
    compbin = "".join(map(str,comp(parse["comp"])))
    jmpbin = "".join(map(str,jmp(parse["jmp"])))

    return head+compbin+dstbin+jmpbin

def dest(s):
    return dest2bin[s]

def comp(s):
    return comp2bin[s]

def jmp(s):
    return jmp2bin[s]

def dec2bin(num):
    b = bin(num)[2:]
    pat = "0" * (15-len(b))
    return pat + b