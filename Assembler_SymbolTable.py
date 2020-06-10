class SymbolTable:
    def __init__(self):
        self.tabel = {}
    
    def addEntry(symbol, address):
        self.tabel[symbol] = address
    
    def contains(symbol):
        return symbol in self.tabel.keys()
    
    def getAddress(symbol):
        return self.tabel[symbol]
    
    def __str__(self):
        return str(self.tabel)