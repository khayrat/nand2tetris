class SymbolTable:
    def __init__(self):
        st = {}
        
        st['SP'] = 0
        st['LCL'] = 1
        st['ARG'] = 2
        st['THIS'] = 3
        st['THAT'] = 4
        st['SCREEN'] = 16384
        st['KBD'] = 24576
        for i in range(16): st['R'+str(i)] = i + 5

        self.st = st
        
    def addEntry(self, symbol, address): self.st[symbol] = address

    def contains(self, symbol): return symbol in self.st

    def getAddress(self, symbol): return self.st[symbol]

if __name__ == '__main__':
    st = SymbolTable()
    print(st.st)
