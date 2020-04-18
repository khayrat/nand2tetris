from parser import Parser
from code import Code

def test_parser(asm_file):
    p=Parser(asm_file)

    print("run parser.....")
    while p.hasMoreCommands():
        print("command type: '%s'" % p.commandType())

        if p.commandType() in ['A_COMMAND', 'L_COMMAND']:
            print("symbol: '%s'" % p.symbol())

        if p.commandType() in ['C_COMMAND']:
            print("dest: '%s'" % p.dest())
            print("comp: '%s'" % p.comp())
            print("jump: '%s'" % p.jump())

        p.advance()
    print("... finished run parser")

def test_parser_with_code(asm_file):
    p=Parser(asm_file)
    c=Code()

    print("run parser with code.....")
    while p.hasMoreCommands():
        if p.commandType() in ['A_COMMAND', 'L_COMMAND']:
            print("symbol: '%s'" % p.symbol())

        if p.commandType() in ['C_COMMAND']:
            print("dest: '%s'" % c.dest(p.dest()))
            print("comp: '%s'" % c.comp(p.comp()))
            print("jump: '%s'" % c.jump(p.jump()))

        p.advance()

def test_assembler_wo_symbols(asm_file):
    a=Assembler(asm_file)
    a.assemble()
