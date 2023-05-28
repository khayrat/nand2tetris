import sys, os, glob
from vm_parser import Parser
from vm_code_writer import CodeWriter

class Translator:
  def __init__(self, src):
    self.src = src
    self.isFile = os.path.isfile(src)
    self.generate_output_fn()

  def generate_output_fn(self):
    if self.isFile:
      fn = self.src
      idx = fn.find(".vm")
      base = fn[:idx]
      self.fn_out =  base + ".asm"
    else:
      self.fn_out =  self.src + '/' + os.path.basename(self.src) + ".asm"
    print("writing to: " + self.fn_out)

  def getInputFiles(self):
    if self.isFile: 
      fns = [self.src]
    else:
      dir_path = self.src + '/*.vm'
      fns = glob.glob(dir_path)
    print("input: " + str(fns))
    return fns

  def translateFile(self, fn):
    with open(fn, 'r') as fin:
      parser = Parser(fin)
      self.parser = parser
      while parser.hasMoreLines():
        parser.advance()
        cmdType = parser.commandType()
        if cmdType == Parser.C_ARITHMETIC:             self.handleArithmeticCommand()
        elif cmdType in [Parser.C_PUSH, Parser.C_POP]: self.handlePushPopCommand()
        elif cmdType == Parser.C_LABEL:                self.handleLabelCommand()
        elif cmdType == Parser.C_GOTO:                 self.handleGotoCommand()
        elif cmdType == Parser.C_IF:                   self.handleIfCommand()
        elif cmdType == Parser.C_FUNCTION:             self.handleFunctionCommand()
        elif cmdType == Parser.C_CALL:                 self.handleCallCommand()
        elif cmdType == Parser.C_RETURN:               self.handleReturnCommand()
    
  def translate(self):
    with open(self.fn_out, 'w') as fh_out:
      #self.cw = CodeWriter(fh=fh_out, fn=self.fn_out)
      self.cw = CodeWriter(fh=fh_out, fn=self.fn_out, bootStrap=True)

      for fn in self.getInputFiles():
        baseName = os.path.splitext(os.path.basename(fn))[0]
        self.cw.setFileName(baseName)
        self.translateFile(fn)
      
      self.cw.close()

  def handleArithmeticCommand(self):
    #print('arithmetic command...')
    p = self.parser
    self.cw.writeArithmetic(p.arg1()) 

  def handlePushPopCommand(self):
    #print('push_pop command...')
    p = self.parser
    self.cw.writePushPop(p.commandType(), p.arg1(), int(p.arg2())) 

  def handleLabelCommand(self):
    #print('label command...')
    p = self.parser
    self.cw.writeLabel(p.arg1()) 

  def handleGotoCommand(self):
    #print('goto command...')
    p = self.parser
    self.cw.writeGoto(p.arg1()) 

  def handleIfCommand(self):
    #print('if command...')
    p = self.parser
    self.cw.writeIf(p.arg1()) 

  def handleFunctionCommand(self):
    #print('function command...')
    p = self.parser
    self.cw.writeFunction(p.arg1(), int(p.arg2())) 

  def handleCallCommand(self):
    #print('call command...')
    p = self.parser
    self.cw.writeCall(p.arg1(), int(p.arg2())) 

  def handleReturnCommand(self):
    #print('return command...')
    p = self.parser
    self.cw.writeReturn()

def main():
  src = sys.argv[1]
  #fn_in = "Test.vm"
  t = Translator(src)
  t.translate()

if __name__ == "__main__":
  main()