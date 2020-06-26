
def writePush(segment,index):
    return "push "+str(segment)+" "+str(index)+"\n"

def writePop(segment,index):
    return "pop "+str(segment)+" "+str(index)+"\n"

def writeArithmetic(command):
     ArithmeticLogicOP = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or',
        '-': 'neg',
        '~': 'not'
    }
    return ArithmeticLogicOP[command]+"\n"

def writeLabel(label):
    return "label "+str(label)+"\n"

def writeGoto(label):
    return "goto "+str(label)+"\n"

def writeIf(label):
    return "if-goto "+str(label)+"\n"

def writeCall(func,argsNum):
    return "call "+str(func)+" "+str(argsNum)+"\n"

def writeFunction(func,localsNum):
    return "function "+str(func)+" "+str(localsNum)+"\n"

def writeReturn():
    return "return"+"\n"