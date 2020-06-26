class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.index = 0

    def reset(self):
        self.symbols = []
        self.index = 0
    
    def define(self,name,stype,kind):
        symbol = {"name":name, "type":stype, "kind":kind, "index":self.index}
        self.index += 1
        self.symbols.append(symbol)
    
    def varCount(self,kind):
        return sum([symbol['kind'] == kind for symbol in self.symbols])

    def kindOf(self,name):
        target = None
        for symbol in self.symbols:
            if symbol['name'] == name:
                target = symbol
        if target:
            return target["kind"]
    
    def typeOf(self,name):
        target = None
        for symbol in self.symbols:
            if symbol['name'] == name:
                target = symbol
        if target:
            return target["type"]
    
    def indexOf(self,name):
        target = None
        for symbol in self.symbols:
            if symbol['name'] == name:
                target = symbol
        if target:
            return target["index"]