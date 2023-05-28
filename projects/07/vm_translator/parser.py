import re, sys

_symbol = '[a-zA-Z:_$0-9.]+'
class Parser:
    def __init__(self, fn=None, stream=None):
        # to be ignored
        self.comment = re.compile("((^\s*//)|(^\s+$)|(^$))")
        # memory access commands
        self.c_push_pop = re.compile('^(push|pop)\s+(\w+)\s+(\d+)$')    
        # program flow commands
        self.c_lable_goto = re.compile('^(label|goto)\s+(' + _symbol +')$')
        self.c_if_goto = re.compile('^(if-goto)\s+(' + _symbol +')$')
        # function calling commands
        self.c_return = re.compile('^return$')
        self.c_fun_call = re.compile('^(call|function)\s+('+_symbol+')(\s+(\d+(\s+\d+)*))?$')
        # arithmetic logical commands
        self.c_arithmetic = re.compile('^(\w+)$')    
        # yieldings
        self.cmdType = None
        self._arg1 = None
        self._arg2 = None
        # internals
        self.fn = fn
        print("parsing file %s" % self.fn)
        with open(fn) as f:
            self.lines = list(f)
        self.len = len(self.lines)
        self.index = 0
        self.lookaheadCmd = self._getNextCmd()
        
    def _getNextCmd(self):
        if self.len == self.index: return None
        
        line = self.lines[self.index].strip()
        self.index += 1
        
        if self.comment.search(line):
            return self._getNextCmd()
        else:
            return line
            
    def hasMoreCommands(self):
        return self.lookaheadCmd != None

    def _decompose(self, cmd):
        self.cmdType = None
        self._arg1 = None
        self._arg2 = None

        #print('cmd: "%s"' % cmd)
       
        # memory access commands 
        m = self.c_push_pop.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_PUSH' if m.group(1) == 'push' else 'C_POP'
            self._arg1 = m.group(2)
            self._arg2 = m.group(3)
            return

        # program flow commands
        # if-goto symbol
        m = self.c_if_goto.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_IF'
            self._arg1 = m.group(2)
            return
        # lable symbol or goto symbol
        m = self.c_lable_goto.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_LABEL' if m.group(1) == 'label' else 'C_GOTO'
            self._arg1 = m.group(2)
            return

        # function calling commands
        # function or call functionName nLocals
        m = self.c_fun_call.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_CALL' if m.group(1) == 'call' else 'C_FUNCTION'
            self._arg1 = m.group(2)
            self._arg2 = m.group(4)
            return
        # return
        m = self.c_return.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_RETURN'
            return

        # arithmetic commands
        m=self.c_arithmetic.search(cmd)
        if m:
            #print("group: %s" % str(m.groups()))
            self.cmdType = 'C_ARITHMETIC'
            self._arg1 = m.group(1)
            return

    def advance(self):
        self._decompose(self.lookaheadCmd)
        self.lookaheadCmd = self._getNextCmd()

    def commandType(self): return self.cmdType
        
    def arg1(self): return self._arg1
    
    def arg2(self): return self._arg2


if __name__ == '__main__':
    fn = sys.argv[1]
    p = Parser(fn)

    while p.hasMoreCommands():
        p.advance()
        t=p.commandType()
        #print("type: %s " % t)
        a1=p.arg1()
        #print("arg1: %s " % a1)
        a2=p.arg2()
        #print("arg2: %s " % a2)
