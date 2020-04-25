from parser import Parser
import sys, os

def test_constructor():
    # existing file
    p=Parser("valid_code.vm")

    # nonexisiting file: should raise execption
    gotException=False
    try:
        p=Parser("foo")
    except OSError:
        gotException=True

    assert gotException

def test_splitter():
    parts = ['aaa', 'bbb', 'ccc']
    assert parts == 'aaa   bbb ccc'.split() 

def test_hasMoreCommands():
    p=Parser("valid_code.vm")
    assert p.hasMoreCommands()
    p=Parser("empty_file.vm")
    assert not p.hasMoreCommands()
    p=Parser("only_commentlines.vm")
    assert not p.hasMoreCommands()
    try: p=Parser("invalid_code.vm")
    except: pass
    else: raise Exception("invalid code not recognized")

def test_advance():
    p=Parser("valid_code.vm")
    while p.hasMoreCommands():
        p.advance()

    p=Parser("invalid_segment.vm")
    try:
        while p.hasMoreCommands():
            p.advance()
    except:
        pass
    else: 
        raise Exception("expected invalid segement exception")

def test_commandType():
    commands = [
        {'cmd': 'C_PUSH', 'arg1': 'local', 'arg2': '1'},
        {'cmd': 'C_PUSH', 'arg1': 'constant', 'arg2': '1'},
        {'cmd': 'C_ARITHMETIC', 'arg1': None, 'arg2': None},
        {'cmd': 'C_POP', 'arg1': 'argument', 'arg2': '3'}
    ]
    idx = 0
    p=Parser("valid_code.vm")
    while p.hasMoreCommands():
        command = commands[idx]
        try:
            assert p.commandType() == command['cmd']
            assert p.arg1() == command['arg1']
            assert p.arg2() == command['arg2']
        except AssertionError:
            print("#### expected for line %s '%s', but got '%s' for line number: %s and line: '%s'" % 
                    (idx, [command['cmd'], command['arg1'], command['arg2']], [p.commandType(), p.arg1(), p.arg2()], p.index, p.line))
            raise
        p.advance()
        idx += 1

if __name__ == '__main__':
    test_constructor()
    test_splitter()
    test_hasMoreCommands()
    test_advance()
    test_commandType()
