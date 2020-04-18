from parser import Parser
from code import Code
from symboltable import SymbolTable

class Assembler:
    def __init__(self, asm_file):
        self.asm_file = asm_file
        self.hack_file = asm_file[:asm_file.rindex('.')+1] + 'hack'
        self.st = SymbolTable() 

    def assemble(self):
        self._firstPass()
        self._secondPass()

    def _firstPass(self):
        p = Parser(self.asm_file)
        st = self.st
        currentLine = 0
        symbolsToBeMapped = []
        while p.hasMoreCommands():
            if p.commandType() == 'A_COMMAND':
                symbol = p.symbol()
                if not symbol.isdigit() and  not self.st.contains(symbol):
                    # to be mapped once all lables are processed
                    symbolsToBeMapped.append(symbol)
                currentLine += 1
            elif p.commandType() == 'L_COMMAND':
                symbol = p.symbol()
                st.addEntry(symbol, currentLine)
            elif p.commandType() == 'C_COMMAND':
                currentLine += 1

            p.advance()

        self._mapSymbols(symbolsToBeMapped)

    def _mapSymbols(self, symbols):
        address = 16
        st = self.st
        for symbol in symbols:
            if not st.contains(symbol):
                st.addEntry(symbol, address)
                address += 1

    def _secondPass(self):
        p = Parser(self.asm_file)
        c = Code()
        st = self.st
        fh = open(self.hack_file, 'w')
        try:
            while p.hasMoreCommands():
                if p.commandType() == 'A_COMMAND':
                    symbol = p.symbol()
                    if symbol.isdigit(): instruction = self._dec2bin(symbol)
                    else:                instruction = self._dec2bin(st.getAddress(symbol))
                    fh.write(instruction + '\n')
                elif p.commandType() in ['C_COMMAND']:
                    dest = c.dest(p.dest())
                    comp = c.comp(p.comp())
                    jump = c.jump(p.jump())
                    instruction = '111' + comp + dest + jump
                    fh.write(instruction + '\n')

                p.advance()
        finally:
            fh.close()

    def _dec2bin(self, dec):
        bits = str(bin(int(dec)))[2:]
        return self._paddTo(bits, 16)

    def _paddTo(self, bits, padding):
        paddedBits = bits
        while len(paddedBits) < padding:
            paddedBits = '0' + paddedBits
        return paddedBits

def main():
    import sys
    a = Assembler(sys.argv[1])
    a.assemble()

if __name__ == '__main__':
    main()
