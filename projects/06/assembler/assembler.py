from parser import Parser
from code import Code

class Assembler:
    def __init__(self, asm_file):
        self.hack_file = asm_file[:asm_file.rindex('.')+1] + 'hack'
        self.parser = Parser(asm_file)
        self.code = Code()

    def assemble(self):
        fh = open(self.hack_file, 'w')
        p = self.parser
        c = self.code
        try:
            while p.hasMoreCommands():
                if p.commandType() == 'A_COMMAND':
                    instruction = self._dec2bin(p.symbol())
                elif p.commandType() == 'L_COMMAND':
                    instruction = self._dec2bin(p.symbol())
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
