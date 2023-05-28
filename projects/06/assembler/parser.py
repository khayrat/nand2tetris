import re

class Parser:
    def __init__(self, fn):
        self.fn = fn
        with open(fn) as f:
            self.lines = list(f)
        self.line = None
        self.len = len(self.lines)
        self.index = 0
        self.comment = re.compile("(//|\s+|^$)")
        self.a_command = re.compile('@([a-zA-Z:_$0-9.]+)')    
        self.c_command = re.compile('((\w+)=)?([10AMD\-+|&!]+)(;(\w{0,3}))?')
        self.l_command = re.compile('\(([a-zA-Z:_$0-9.]+)\)')
        self.lookaheadCmd = self._getNextCmd()
        self.cmd = None
        self._dest = None
        self._jump = None
        
    def _getNextCmd(self):
        if self.len == self.index: return None
        
        l = self.lines[self.index].strip()
        self.index += 1
        
        if self.comment.search(l):
            return self._getNextCmd()
        else:
            self.line = l
            return l
            
    def hasMoreCommands(self):
        return self.lookaheadCmd != None

    def _decompose(self, cmd):
        self.cmdType = None
        self.cmd = None
        self._symbol = None
        self._dest = None
        self._comp = None
        self._jump = None

        #print('cmd: "%s"' % cmd)
        
        m=self.a_command.search(cmd)
        if m:
            self.cmdType = 'A_COMMAND'
            self._symbol = m.group(1)
            return


        m = self.l_command.search(cmd)
        if m:
            self.cmdType = 'L_COMMAND'
            self._symbol = m.group(1)
            return

        m = self.c_command.search(cmd) 
        if m:
            self.cmdType = 'C_COMMAND'
            #print("group: %s" % str(m.groups()))
            groups = m.groups()
            if groups[1] != None:
                self._dest = groups[1]
            if groups[2] != None:
                self._comp = groups[2]
            if groups[4] != None:
                self._jump = groups[4]
            return

    def advance(self):
        self._decompose(self.lookaheadCmd)
        self.lookaheadCmd = self._getNextCmd()

    def commandType(self): return self.cmdType
        
    def symbol(self): return self._symbol

    def dest(self): return self._dest

    def comp(self): return self._comp

    def jump(self): return self._jump

    def reset(self):
        self.line = None
        self.index = 0
        self.lookaheadCmd = self._getNextCmd()
        self.cmd = None
        self._dest = None
        self._jump = None

if __name__ == '__main__':
    fn = 'Test.asm'
    p = Parser(fn)

    while p.hasMoreCommands():
        p.advance()
        t=p.commandType()
        print("type: %s " % t)
        s=p.symbol()
        print("symbol: %s" % s)
        d=p.dest()
        print("dest: %s " % d)
        c=p.comp()
        print("comp: %s" % c)
        j=p.jump()
        print("jump: %s" % j)
