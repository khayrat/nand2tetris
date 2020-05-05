from codewriter import CodeWriter
    
def test_constructor():
    c=CodeWriter("out.asm")
    c.close()

def test_memCommand():
    c=CodeWriter("out.asm")
    #cmds = ['C_PUSH']
    cmds = ['C_POP']
    #cmds = ['C_PUSH', 'C_POP']
    segments = ['local']
    #segments = ['local', 'argument', 'this', 'that', 'constant', 'static', 'temp', 'pointer']
    index = ['5']
    #index = ['1', '5']

    def invoke(cmd, arg1, arg2):
        print("calling: %s %s %s" % (cmd, arg1, arg2))
        c.writePushPop(cmd, arg1, arg2)

    [invoke(c, s, i) for c in cmds for s in segments for i in index]
    c.close()

if __name__ == '__main__':
    test_constructor()
    test_memCommand()
