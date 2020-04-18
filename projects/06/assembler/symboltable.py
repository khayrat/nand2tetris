class SymbolTable:
    def __init__(self):
        self.st = self._initST()

    def _initST(self):
        st = {
                'SP': '0',
                'LCL': '1',
                'ARG': '2',
                'THIS': '3',
                'THAT': '4',
                'SCREEN': '16384',
                'KBD': '24576'
        }

        for i in range(16):
            st['R' + str(i)] = str(i)

        return st

    def addEntry(self, symbol, address):
        '''
        Adds the pair (symbol, address) to the table.
        '''
        self.st[symbol] = address 

    def contains(self, symbol):
        '''
        Does the symbol table contain the given symbol?
        '''
        return symbol in self.st


    def getAddress(self, symbol):
        '''
        Returns the address associated with the symbol.
        '''
        return self.st[symbol]
