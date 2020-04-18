from parser import Parser

def test(asm_file):
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
