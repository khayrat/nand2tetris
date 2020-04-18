from assembler import Assembler

def test_firstPass():
    a=Assembler('firstPass.asm')
    a._firstPass()
    symbols = ['i', 'loop', 'END', '4711', 'sum'] 
    for s in symbols:
        if a.st.contains(s):
            print("'%s': '%s'" % (s, a.st.getAddress(s)))
