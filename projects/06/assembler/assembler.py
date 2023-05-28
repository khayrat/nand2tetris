from parser import Parser
from code import Code
from symbolTable import SymbolTable
import sys

class Assembler:
  def __init__(self, fn):
    self.infn = fn
    self.outfn = fn[:-3] + 'hack'
    self.p = Parser(fn)
    self.c = Code()
    self.st = SymbolTable()
    self.line = 0
    self._offset = 16
    self._syms = 0
    self.code = []

  def assemble(self):
    self._firstPass()
    self.p.reset()
    self._secondPass()

  def _firstPass(self):
    p = self.p
    c = self.c
    code = self.code
    while p.hasMoreCommands():
        p.advance()
        t=p.commandType()

        if t == 'C_COMMAND':
          self.line += 1
        elif t == 'A_COMMAND':
          self.line += 1
        elif t == 'L_COMMAND':
          self._addLabel(p.symbol())
        else:
          self._error()

  def _secondPass(self):
    p = self.p
    c = self.c
    code = self.code
    while p.hasMoreCommands():
        p.advance()
        t=p.commandType()

        if t == 'C_COMMAND':
          dest = c.dest(p.dest())
          if dest == None: self._error()
  
          if p.comp() == None: self._error()          
          comp = c.comp(p.comp())
          if comp == None: self._error()
            
          jump = c.jump(p.jump())
          if jump == None: self._error()

          code.append(comp+dest+jump)

          self.line += 1
        elif t == 'A_COMMAND':
          acommand = self._aCommand(p.symbol())
          code.append(acommand)
          self.line += 1
        elif t == 'L_COMMAND':
          continue
        else:
          self._error()

    self._writeout()

  def _error(self):
    print("invalid command near line %d: %s" % (self.p.index, self.p.line))
    sys.exit(1)

  def _resolve(self, symbol):
    if symbol.isdigit():
      return symbol
    else:
      st = self.st
      if not st.contains(symbol):
        st.addEntry(symbol, self._getAddrAndUpdate())
      return st.getAddress(symbol)
    
  def _addLabel(self, symbol):
    self.st.addEntry(symbol, self.line)
    
  def _aCommand(self, symbol):
    padding = '0' * 16
    val = self._resolve(symbol)

    #print(padding)
    b = str(bin(int(val)))[2:]
      
    return padding[:-len(b)] + b

  def _getAddrAndUpdate(self):
    addr = self._offset + self._syms
    self._syms += 1
    return addr

  def _writeout(self):
      with open(self.outfn, 'w') as f:
        f.writelines([l+'\n' for l in self.code]) 

if __name__ == '__main__':
  fn = sys.argv[1]
  a = Assembler(fn)
  a.assemble()
