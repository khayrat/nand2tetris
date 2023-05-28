from parser import Parser
from code_writer import CodeWriter
import sys, os

class VM:
  def __init__(self, fn):
    self.infn = fn

  def emulate(self):
    outfn = None
    if os.path.isdir(self.infn):
      outfn = self.infn + '.asm'
      c = CodeWriter(outfn)
      for file in os.listdir(self.infn):
        if file.endswith('.vm'):
          p = Parser(self.infn +'/' + file)  
          self._emulate(p, c, file.name)
    else:
      outfn = self.infn[:-2] + 'asm'
      c = CodeWriter(outfn)
      p = Parser(self.infn)  
      self._emulate(p, c, self.infn)

  def _emulate(self, p, c, f):
    c.setFileName(f.split('/')[-1])
    while(p.hasMoreCommands()):
      p.advance() 
      type = p.commandType()
      if type == 'C_ARITHMETIC':
        c.writeArithmetic(p.arg1())
      elif type in ['C_PUSH', 'C_POP']:
        c.writePushPop(type, p.arg1(), p.arg2())
      else:
        self._error(type)

  def _error(cmd):
    print("invalid command: %s" % (type))
    #print("invalid command near line %d: %s" % (self.p.index, self.p.line))
    sys.exit(1)

if __name__ == '__main__':
  fn = sys.argv[1]
  vm = VM(fn)
  vm.emulate()
