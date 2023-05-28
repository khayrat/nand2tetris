import sys
from vm_parser import Parser
from vm_code_writer import CodeWriter

class Translator:
  def __init__(self, fn_in):
    self.fn_in = fn_in
    self.generate_fn()

  def generate_fn(self):
    fn = self.fn_in
    idx = fn.find(".vm")
    base = fn[:idx]
    self.fn_out =  base + ".asm"
    print("writing to: " + self.fn_out)

  def translate(self):
    with open(self.fn_out, 'w') as fh_out:
      self.cw = CodeWriter(fh=fh_out, fn=self.fn_out)

      with open(self.fn_in, 'r') as fin:
        parser = Parser(fin)
        self.parser = parser
        while parser.hasMoreLines():
          parser.advance()
          cmdType = parser.commandType()
          if cmdType == Parser.C_ARITHMETIC:
            self.handleArithmeticCommand()
          elif cmdType in [Parser.C_PUSH, Parser.C_POP]: self.handlePushPopCommand()
      
      self.cw.close()

  def handleArithmeticCommand(self):
    #print('arithmetic command...')
    self.cw.writeArithmetic(self.parser.arg1()) 

  def handlePushPopCommand(self):
    #print('push_pop command...')
    p = self.parser
    self.cw.writePushPop(p.commandType(), p.arg1(), int(p.arg2())) 

def main():
  fn_in = sys.argv[1]
  #fn_in = "Test.vm"
  t = Translator(fn_in)
  t.translate()

if __name__ == "__main__":
  main()